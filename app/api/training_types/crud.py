from sqlalchemy.orm import Session
from app.api.training_types import models


def get_training_types(db: Session):
    return db.query(models.TrainingType).all()
