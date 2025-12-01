from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import settings
from app.models.user import User
from app.models.token import Token as TokenModel
from app.schemas.user import UserCreate, UserResponse, LoginRequest, Token

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    hashed_password = get_password_hash(user_data.password)

    new_user = User(
        username=user_data.username,
        passwordhash=hashed_password,
        email=user_data.email,
        fullname=user_data.fullname,
        role="User"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == login_data.username).first()

    if not user or not verify_password(login_data.password, user.passwordhash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    expires_at = datetime.utcnow() + access_token_expires
    db_token = TokenModel(
        token=access_token,
        iduser=user.id,
        expiresat=expires_at,
        isrevoked=False
    )
    db.add(db_token)
    db.commit()

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
def logout(token: str, db: Session = Depends(get_db)):
    db_token = db.query(TokenModel).filter(TokenModel.token == token).first()

    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Token not found"
        )

    db_token.isrevoked = True
    db.commit()

    return {"message": "Successfully logged out"}
