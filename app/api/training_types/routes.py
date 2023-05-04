from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.training_types import schemas, crud
from app.dependencies import get_db


router = APIRouter(tags=["trainingtypes"])


@router.get("/trainingtypes", response_model=list[schemas.TrainingType])
def get_training_types(db: Session = Depends(get_db)):
    return crud.get_training_types(db=db)
