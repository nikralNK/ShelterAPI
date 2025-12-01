from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.deps import get_current_user, get_current_admin_user
from app.models.animal import Animal
from app.models.user import User
from app.schemas.animal import AnimalCreate, AnimalUpdate, AnimalResponse

router = APIRouter()

@router.get("/", response_model=List[AnimalResponse])
def get_animals(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    type: Optional[str] = None,
    gender: Optional[str] = None,
    size: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Animal)

    if type:
        query = query.filter(Animal.type == type)
    if gender:
        query = query.filter(Animal.gender == gender)
    if size:
        query = query.filter(Animal.size == size)
    if status:
        query = query.filter(Animal.currentstatus == status)

    animals = query.offset(skip).limit(limit).all()
    return animals

@router.get("/{animal_id}", response_model=AnimalResponse)
def get_animal(animal_id: int, db: Session = Depends(get_db)):
    animal = db.query(Animal).filter(Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Animal not found"
        )
    return animal

@router.post("/", response_model=AnimalResponse, status_code=status.HTTP_201_CREATED)
def create_animal(
    animal_data: AnimalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    new_animal = Animal(
        name=animal_data.name,
        type=animal_data.type,
        breed=animal_data.breed,
        dateofbirth=animal_data.dateofbirth,
        idenclosure=animal_data.idenclosure,
        gender=animal_data.gender,
        size=animal_data.size,
        temperament=animal_data.temperament,
        currentstatus="Доступен"
    )

    db.add(new_animal)
    db.commit()
    db.refresh(new_animal)

    return new_animal

@router.put("/{animal_id}", response_model=AnimalResponse)
def update_animal(
    animal_id: int,
    animal_update: AnimalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    animal = db.query(Animal).filter(Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Animal not found"
        )

    if animal_update.name is not None:
        animal.name = animal_update.name
    if animal_update.type is not None:
        animal.type = animal_update.type
    if animal_update.breed is not None:
        animal.breed = animal_update.breed
    if animal_update.dateofbirth is not None:
        animal.dateofbirth = animal_update.dateofbirth
    if animal_update.idenclosure is not None:
        animal.idenclosure = animal_update.idenclosure
    if animal_update.idguardian is not None:
        animal.idguardian = animal_update.idguardian
    if animal_update.currentstatus is not None:
        animal.currentstatus = animal_update.currentstatus
    if animal_update.gender is not None:
        animal.gender = animal_update.gender
    if animal_update.size is not None:
        animal.size = animal_update.size
    if animal_update.temperament is not None:
        animal.temperament = animal_update.temperament
    if animal_update.photo is not None:
        animal.photo = animal_update.photo

    db.commit()
    db.refresh(animal)

    return animal

@router.delete("/{animal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_animal(
    animal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    animal = db.query(Animal).filter(Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Animal not found"
        )

    db.delete(animal)
    db.commit()

    return None
