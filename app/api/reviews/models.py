from pydantic import BaseModel, Field
from uuid import uuid4

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


class ReviewAverageScoreResponse(BaseModel):
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
