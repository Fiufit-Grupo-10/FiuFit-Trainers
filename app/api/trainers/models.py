from enum import Enum
from pydantic import BaseModel, Field
from uuid import uuid4

MAX_TITLE_LENGTH = 200
MIN_TITLE_LENGTH = 3
MAX_DESCRIPTION_LENGTH = 5000


class Difficulty(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class TrainingPlan(BaseModel):
    id: str = Field(default_factory=uuid4, alias="_id")
    trainer: str = Field(...)  # User uuid
    title: str = Field(..., min_length=MIN_TITLE_LENGTH, max_length=MAX_TITLE_LENGTH)
    description: str | None = Field(default=None, max_length=MAX_DESCRIPTION_LENGTH)
    difficulty: Difficulty
    training_types: list[str] = Field(...)
    goals: list = Field(...)
    duration: int = Field(...)
    blocked: bool = Field(default=False)
    favourited_by: list[str] = Field(default=[])

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "trainer": "c59710ef-f5d0-41ba-a787-ad8eb739ef4c",
                "title": "Sample training plan",
                "description": "Training plan description",
                "difficulty": "beginner",
                "training_types": ["cardio"],
                "goals": [
                    {
                        "name": "123123",
                        "category": "Repeticiones",
                        "amount": "123",
                        "media": ["imagen.com"],
                    }
                ],
                "duration": 90,
                "reviews": None,
                "blocked": False,
                "favourited_by": ["7ca0fa95-af47-40b4-8e39-2fae5ee2667a" ""],
            }
        }


class BlockTrainingPlan(BaseModel):
    uid: str = Field(...)
    blocked: bool = Field(...)


class UpdateTrainingPlan(BaseModel):
    title: str | None = Field(
        default=None, min_length=MIN_TITLE_LENGTH, max_length=MAX_TITLE_LENGTH
    )
    description: str | None = Field(default=None, max_length=MAX_DESCRIPTION_LENGTH)
    difficulty: Difficulty | None
    training_types: list[str] | None = Field(default=None)
    goals: list | None = None
    duration: int | None = Field(default=None)
    blocked: bool | None = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "title": "Sample training plan",
                "description": "Training plan description",
                "difficulty": "advanced",
                "training_types": ["cardio"],
                "goals": [
                    {
                        "name": "123123",
                        "category": "Repeticiones",
                        "amount": "123",
                        "media": ["imagen.com"],
                    }
                ],
                "duration": 30,
                "blocked": False,
            }
        }


class UpdateFavourite(BaseModel):
    training_id: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "training_id": "7ca0fa95-af47-40b4-8e39-2fae5ee2667a",
            }
        }
