from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.deps import get_current_user, get_current_admin_user
from app.models.application import Application
from app.models.user import User
from app.schemas.application import ApplicationCreate, ApplicationUpdate, ApplicationResponse

router = APIRouter()

@router.get("/", response_model=List[ApplicationResponse])
def get_applications(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    query = db.query(Application)

    if status_filter:
        query = query.filter(Application.status == status_filter)

    applications = query.offset(skip).limit(limit).all()
    return applications

@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    return application

@router.post("/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(
    application_data: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_application = Application(
        idanimal=application_data.idanimal,
        idguardian=application_data.idguardian,
        comments=application_data.comments,
        status="На рассмотрении"
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application

@router.put("/{application_id}", response_model=ApplicationResponse)
def update_application(
    application_id: int,
    application_update: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    if application_update.status is not None:
        application.status = application_update.status
    if application_update.comments is not None:
        application.comments = application_update.comments

    db.commit()
    db.refresh(application)

    return application

@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    db.delete(application)
    db.commit()

    return None
