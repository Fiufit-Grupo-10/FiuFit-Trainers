from enum import Enum
from pydantic import BaseModel, Field, PyObject
from uuid import uuid4, UUID


# class PyObjectId(ObjectId):
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate

#     @classmethod
#     def validate(cls, v):
#         if not ObjectId.is_valid(v):
#             raise ValueError("Invalid objectid")
#         return ObjectId(v)

#     @classmethod
#     def __modify_schema__(cls, field_schema):
#         field_schema.update(type="string")
        

MAX_TITLE_LENGTH = 200
MIN_TITLE_LENGTH = 3
MAX_DESCRIPTION_LENGTH = 5000


class Difficulty(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"

    
class TrainingPlan(BaseModel):
    id: UUID = Field(default_factory=uuid4, alias="_id")
    creator: UUID = Field(...) #User uuid
    title: str = Field(..., min_length=MIN_TITLE_LENGTH, max_length=MAX_TITLE_LENGTH)
    description: str | None = Field(default=None, max_length=MAX_DESCRIPTION_LENGTH)
    difficulty: Difficulty 
    training_types: list[str] = Field(...)
    media: list[str] | None = Field(default=None, description="Multimedia resources (urls) associated with the training plan")
    # Goals => ejercicios + tiempo + mas descanso
    goals: list[str]
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example":
            {
            "id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
            "creator": "c59710ef-f5d0-41ba-a787-ad8eb739ef4c",
            "title": "Sample training plan",
            "description": "Training plan description",
            "difficulty": "beginner",
            "media": ["link-to-image", "link-to-video"],
            "goals": ["plank: one minute"]
        }
    }
    

class UpdateTrainingPlan(BaseModel):
    title: str | None = Field(default=None,min_length=MIN_TITLE_LENGTH, max_length=MAX_TITLE_LENGTH) 
    description: str | None = Field(default=None, max_length=MAX_DESCRIPTION_LENGTH)
    difficulty: Difficulty | None
    training_types: list[str] | None = Field(default=None)
    media: list[str] | None = Field(default=None, description="Multimedia resources (urls) associated with the training plan")
    goals: list[str] | None = None
