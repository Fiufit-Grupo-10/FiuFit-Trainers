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


REVIEW_MAX_LENGTH = 240


class Review(BaseModel):
    id: str = Field(default_factory=uuid4, alias="_id")
    plan_id: str = Field(...)
    user_id: str = Field(...)
    review: str | None = Field(default=None, max_length=REVIEW_MAX_LENGTH)
    score: int = Field(..., gt=0, le=5)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "plan_id": "c59710ef-f5d0-41ba-a787-ad8eb739ef4c",
                "user_id": "7ca0fa95-af47-40b4-8e39-2fae5ee2667a",
                "review": "Some review",
                "score": 4,
            }
        }


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
    duration: int | None = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "title": "Sample training plan",
                "description": "Training plan description",
                "difficulty": "hard",
                "training_types": ["cardio"],
                "media": ["link-to-image", "link-to-video"],
                "goals": ["plank: one minute"],
                "duration": 30,
            }
        }


class ReviewResponse(BaseModel):
    reviews: list[Review]

    class Config:
        schema_extra = {
            "example": {
                "reviews": [
                    {
                        "plan_id": "c59710ef-f5d0-41ba-a787-ad8eb739ef4c",
                        "user_id": "7ca0fa95-af47-40b4-8e39-2fae5ee2667a",
                        "review": "Some review",
                        "score": 4,
                    },
                    {
                        "plan_id": "c59710ef-f5d0-41bc-a787-ad8eb739ef4d",
                        "user_id": "9ca0fa95-a847-40b4-8e39-2fae5ee2667a",
                        "review": "Another review",
                        "score": 3,
                    },
                ]
            }
        }


class ReviewMeanResponse(BaseModel):
    mean: float = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "mean": 4.5,
            }
        }


class UpdateReview(BaseModel):
    review: str | None = Field(default=None, max_length=REVIEW_MAX_LENGTH)
    score: int | None = Field(..., gt=0, le=5)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "review": "Updated review",
                "score": 5,
            }
        }
