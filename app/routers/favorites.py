from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.favorite import Favorite
from app.models.user import User
from app.schemas.favorite import FavoriteCreate, FavoriteResponse

router = APIRouter()

@router.get("/", response_model=List[FavoriteResponse])
def get_user_favorites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    favorites = db.query(Favorite).filter(Favorite.iduser == current_user.id).all()
    return favorites

@router.post("/", response_model=FavoriteResponse, status_code=status.HTTP_201_CREATED)
def add_to_favorites(
    favorite_data: FavoriteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_favorite = db.query(Favorite).filter(
        Favorite.iduser == current_user.id,
        Favorite.idanimal == favorite_data.idanimal
    ).first()

    if existing_favorite:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Animal already in favorites"
        )

    new_favorite = Favorite(
        iduser=current_user.id,
        idanimal=favorite_data.idanimal
    )

    db.add(new_favorite)
    db.commit()
    db.refresh(new_favorite)

    return new_favorite

@router.delete("/{favorite_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_favorites(
    favorite_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    favorite = db.query(Favorite).filter(
        Favorite.id == favorite_id,
        Favorite.iduser == current_user.id
    ).first()

    if not favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favorite not found"
        )

    db.delete(favorite)
    db.commit()

    return None

@router.delete("/animal/{animal_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_favorites_by_animal(
    animal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    favorite = db.query(Favorite).filter(
        Favorite.iduser == current_user.id,
        Favorite.idanimal == animal_id
    ).first()

    if not favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favorite not found"
        )

    db.delete(favorite)
    db.commit()

    return None
