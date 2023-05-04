from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.api.admins import schemas, models


def get_training_types(db: Session):
    return db.query(models.TrainingType).all()


def create_admin(db: Session, admin: schemas.AdminCreate) -> models.Admin:
    try:
        new_admin = models.Admin(
            uid=admin.uid, email=admin.email, username=admin.username
        )
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        return new_admin
    except IntegrityError as e:
        raise_integrity_error(
            e, uid=admin.uid, username=admin.username, email=admin.email, type="Admin"
        )


def get_admin(db: Session, uid: str) -> models.Admin:
    return db.query(models.Admin).filter(models.Admin.uid == uid).first()


def get_admins(db: Session):
    return db.query(models.Admin).all()


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
