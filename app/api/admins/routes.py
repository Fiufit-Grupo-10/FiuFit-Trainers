from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud
from app.dependencies import get_db
from . import schemas


router = APIRouter(tags=["admins"])


@router.post("/admins", response_model=schemas.AdminResponse)
def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    return crud.create_admin(db=db, admin=admin)


@router.get("/admins", response_model=list[schemas.AdminResponse])
def get_admins(db: Session = Depends(get_db)):
    return crud.get_admins(db=db)


@router.get("/admins/{user_id}", response_model=schemas.AdminResponse)
def get_admin(user_id: str, db: Session = Depends(get_db)):
    admin = crud.get_admin(db=db, uid=user_id)
    if admin is None:
        detail = f"Admin {user_id} not found"
        raise HTTPException(status_code=404, detail=detail)
    return admin
