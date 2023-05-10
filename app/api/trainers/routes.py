from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.users import crud, schemas
from app.dependencies import get_db


router = APIRouter(tags=["plans"])


@router.post("/plans")
def create_user(plan: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=plan)


@router.put("/plans/{plan_id}")
def update_user(plan_id: schemas.UserRequest, user_id: str, db: Session = Depends(get_db)):
    if crud.get_user(db=db, user_id=user_id) is None:
        detail = f"User {user_id} not found"
        raise HTTPException(status_code=404, detail=detail)
    return crud.update_user(db=db, user=plan_id, uid=user_id)


@router.get("/plans/{plan_id}", response_model=schemas.UserReturn)
def get_user(plan_id: str, db: Session = Depends(get_db)):
    user = crud.get_user(db=db, user_id=plan_id)
    if user is None:
        detail = f"User {plan_id} not found"
        raise HTTPException(status_code=404, detail=detail)
    return user


@router.get("/plans", response_model=list[schemas.UserReturn])
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db=db)
