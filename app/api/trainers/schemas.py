from datetime import date
from enum import Enum
from pydantic import BaseModel, Field, validator


class UserTrainingType(BaseModel):
    username: str
    trainingtype: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    username: str


class Gender(str, Enum):
    M = "M"
    F = "F"
    U = "U"


class UserRequest(UserBase):
    birthday: date | None = Field(default=None, description="format YYYY-MM-DD")
    level: str | None = None
    latitude: int | None = None
    longitude: int | None = None
    height: int | None = Field(default=None, description="unit: cm")
    weight: int | None = Field(default=None, description="unit: kg")
    gender: Gender | None = Field(default=None, max_length=1)
    target: str | None = None
    trainingtypes: list[str] | None = None
    user_type: str | None = Field(default=None, max_length=7)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "email": "user@mail.com",
                "username": "user",
                "birthday": "2000-12-21",
                "level": "amateur",
                "latitude": 1000,
                "longitude": 1000,
                "height": 180,
                "weight": 80,
                "gender": "M",
                "target": "loss fat",
                "trainingtypes": ["Cardio"],
                "user_type": "athlete",
            }
        }


class UserCreate(UserRequest):
    uid: str


