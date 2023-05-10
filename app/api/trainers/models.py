from enum import Enum
from bson import ObjectId
from pydantic import BaseModel, Field, PyObject


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")
        

MAX_TITLE_LENGTH = 200
MIN_TITLE_LENGTH = 3
MAX_DESCRIPTION_LENGTH = 5000


class Difficulty(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"

class Type(BaseModel):
    name: str = Field(...)
    description: str = Field(...)
    
class TrainingPlan(BaseModel):
    id: PyObjectId  = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(..., min_length=MIN_TITLE_LENGTH, max_length=MAX_TITLE_LENGTH)
    description: str | None = Field(default=None, max_length=MAX_DESCRIPTION_LENGTH)
    difficulty: Difficulty = Field(..., ge=1, le=10, description="Training dificulty, 1 is easy 10 is hard")
    training_types: list[Type] = Field(...)
    media: list[str] | None = Field(default=None, description="Multimedia resources (urls) associated with the training plan")
    # Goals => ejercicios + tiempo + mas descanso
    goals: list[str] = Field(...)
