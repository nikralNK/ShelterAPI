from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.deps import get_current_veterinarian_user, get_current_user
from app.models.user import User
from app.models.medical_record import MedicalRecord
from app.models.veterinarian import Veterinarian
from app.models.animal import Animal
from app.schemas.medical_record import MedicalRecordCreate, MedicalRecordResponse, MedicalRecordUpdate

router = APIRouter()

@router.post("/", response_model=MedicalRecordResponse, status_code=status.HTTP_201_CREATED)
def create_medical_record(
    record: MedicalRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_veterinarian_user)
):
    animal = db.query(Animal).filter(Animal.id == record.idanimal).first()
    if not animal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Animal not found"
        )

    veterinarian = db.query(Veterinarian).filter(Veterinarian.iduser == current_user.id).first()
    if not veterinarian:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veterinarian profile not found"
        )

    new_record = MedicalRecord(
        idanimal=record.idanimal,
        idveterinarian=veterinarian.id,
        diagnosis=record.diagnosis,
        treatment=record.treatment,
        notes=record.notes
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return new_record

@router.get("/", response_model=List[MedicalRecordResponse])
def get_medical_records(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    animal_id: int = None
):
    query = db.query(MedicalRecord)
    if animal_id:
        query = query.filter(MedicalRecord.idanimal == animal_id)

    records = query.offset(skip).limit(limit).all()
    return records

@router.get("/{record_id}", response_model=MedicalRecordResponse)
def get_medical_record(
    record_id: int,
    db: Session = Depends(get_db)
):
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical record not found"
        )
    return record

@router.put("/{record_id}", response_model=MedicalRecordResponse)
def update_medical_record(
    record_id: int,
    record_update: MedicalRecordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_veterinarian_user)
):
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical record not found"
        )

    veterinarian = db.query(Veterinarian).filter(Veterinarian.iduser == current_user.id).first()
    if not veterinarian or record.idveterinarian != veterinarian.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own medical records"
        )

    update_data = record_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(record, field, value)

    db.commit()
    db.refresh(record)
    return record

@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_medical_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_veterinarian_user)
):
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical record not found"
        )

    veterinarian = db.query(Veterinarian).filter(Veterinarian.iduser == current_user.id).first()
    if not veterinarian or record.idveterinarian != veterinarian.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own medical records"
        )

    db.delete(record)
    db.commit()
    return None
