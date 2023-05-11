from enum import Enum
from pydantic import BaseModel, Field, PyObject
from uuid import uuid4

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


REVIEW_MAX_LENGTH = 240


class Review(BaseModel):
    uid: str
    username: str
    review: str | None = Field(default=None, max_length=REVIEW_MAX_LENGTH)
    score: int = Field(..., gt=0, le=5)


class TrainingPlan(BaseModel):
    id: str = Field(default_factory=uuid4, alias="_id")
    trainer: str = Field(...)  # User uuid
    title: str = Field(..., min_length=MIN_TITLE_LENGTH, max_length=MAX_TITLE_LENGTH)
    description: str | None = Field(default=None, max_length=MAX_DESCRIPTION_LENGTH)
    difficulty: Difficulty
    training_types: list[str] = Field(...)
    media: list[str] | None = Field(
        default=None,
        description="Multimedia resources (urls) associated with the training plan",
    )
    goals: list[str] = Field(...)
    duration: int = Field(...)
    reviews: list[Review] | None = Field(default=None)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "trainer": "c59710ef-f5d0-41ba-a787-ad8eb739ef4c",
                "title": "Sample training plan",
                "description": "Training plan description",
                "difficulty": "beginner",
                "training_types": ["cardio"],
                "media": ["link-to-image", "link-to-video"],
                "goals": ["plank: one minute"],
                "duration": 90,
                "reviews": None,
            }
        }


class UpdateTrainingPlan(BaseModel):
    title: str | None = Field(
        default=None, min_length=MIN_TITLE_LENGTH, max_length=MAX_TITLE_LENGTH
    )
    description: str | None = Field(default=None, max_length=MAX_DESCRIPTION_LENGTH)
    difficulty: Difficulty | None
    training_types: list[str] | None = Field(default=None)
    media: list[str] | None = Field(
        default=None,
        description="Multimedia resources (urls) associated with the training plan",
    )
    goals: list[str] | None = None

    class Config:
        schema_extra = {
            "example": {
                "title": "Sample training plan",
                "description": "Training plan description",
                "difficulty": "beginner",
                "media": ["link-to-image", "link-to-video"],
                "goals": ["plank: one minute"],
            }
        }
