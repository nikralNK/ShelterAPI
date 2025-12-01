from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.deps import get_current_admin_user
from app.core.security import get_password_hash
from app.models.user import User
from app.models.veterinarian import Veterinarian
from app.schemas.veterinarian import VeterinarianCreate, VeterinarianResponse, VeterinarianUpdate

router = APIRouter()

@router.post("/", response_model=VeterinarianResponse, status_code=status.HTTP_201_CREATED)
def create_veterinarian(
    veterinarian: VeterinarianCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    existing_user = db.query(User).filter(User.username == veterinarian.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    new_user = User(
        username=veterinarian.username,
        passwordhash=get_password_hash(veterinarian.password),
        email=veterinarian.email,
        fullname=veterinarian.fullname,
        role="Veterinarian"
    )
    db.add(new_user)
    db.flush()

    new_veterinarian = Veterinarian(
        fullname=veterinarian.fullname,
        specialization=veterinarian.specialization,
        phonenumber=veterinarian.phonenumber,
        licensenumber=veterinarian.licensenumber,
        iduser=new_user.id
    )
    db.add(new_veterinarian)
    db.commit()
    db.refresh(new_veterinarian)

    return new_veterinarian

@router.get("/", response_model=List[VeterinarianResponse])
def get_veterinarians(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    veterinarians = db.query(Veterinarian).offset(skip).limit(limit).all()
    return veterinarians

@router.get("/{veterinarian_id}", response_model=VeterinarianResponse)
def get_veterinarian(
    veterinarian_id: int,
    db: Session = Depends(get_db)
):
    veterinarian = db.query(Veterinarian).filter(Veterinarian.id == veterinarian_id).first()
    if not veterinarian:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veterinarian not found"
        )
    return veterinarian

@router.put("/{veterinarian_id}", response_model=VeterinarianResponse)
def update_veterinarian(
    veterinarian_id: int,
    veterinarian_update: VeterinarianUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    veterinarian = db.query(Veterinarian).filter(Veterinarian.id == veterinarian_id).first()
    if not veterinarian:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veterinarian not found"
        )

    update_data = veterinarian_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(veterinarian, field, value)

    db.commit()
    db.refresh(veterinarian)
    return veterinarian

@router.delete("/{veterinarian_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_veterinarian(
    veterinarian_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    veterinarian = db.query(Veterinarian).filter(Veterinarian.id == veterinarian_id).first()
    if not veterinarian:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veterinarian not found"
        )

    if veterinarian.iduser:
        user = db.query(User).filter(User.id == veterinarian.iduser).first()
        if user:
            db.delete(user)

    db.delete(veterinarian)
    db.commit()
    return None
