from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from . import models, schemas


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    try:
        new_user = models.User(uid=user.uid, email=user.email, username=user.username)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError as e:
        raise_integrity_error(
            e, uid=user.uid, username=user.username, email=user.email, type="User"
        )


def update_user(db: Session, user: schemas.UserRequest, uid: str) -> models.User:
    old_user = get_user(db, uid)
    update_user_training_types(db, user)
    old_user.height = user.height
    old_user.weight = user.weight
    old_user.gender = user.gender
    old_user.target = user.target
    old_user.birthday = user.birthday
    old_user.level = user.level
    old_user.latitude = user.latitude
    old_user.longitude = user.longitude
    old_user.user_type = user.user_type
    db.commit()
    db.refresh(old_user)
    return old_user


def update_user_training_types(db: Session, user: schemas.UserRequest):
    rows_to_delete = (
        db.query(models.UserTrainingType).filter_by(username=user.username).all()
    )
    for row in rows_to_delete:
        db.delete(row)
    if user.trainingtypes is None:
        return
    for trainingtype in user.trainingtypes:
        db.add(
            models.UserTrainingType(username=user.username, trainingtype=trainingtype)
        )
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=404, detail=f"TrainingType {trainingtype} not found"
        )


def get_user(db: Session, user_id: str) -> models.User:
    return db.query(models.User).filter(models.User.uid == user_id).first()


def get_users(db: Session):
    return db.query(models.User).all()


def raise_integrity_error(
    e: IntegrityError,
    uid: int | None,
    username: str | None,
    email: str | None,
    type: str,
):
    if "uid" in str(e.orig.args):
        detail = f"{type} with uid: {uid} already exists"
    elif "username" in str(e.orig.args):
        detail = f"{type} with username: {username} already exists"
    else:
        detail = f"{type} with email: {email} already exists"
    raise HTTPException(status_code=409, detail=detail)
