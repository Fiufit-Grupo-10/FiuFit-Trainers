from app.api.reviews.models import (
    Review,
    ReviewAverageScoreResponse,
    ReviewResponse,
    UpdateReview,
)
from app.config.database import REVIEWS_COLLECTION_NAME, TRAININGS_COLLECTION_NAME
from fastapi.encoders import jsonable_encoder
from fastapi import Request


async def create_review(r: Request, review: Review) -> Review | None:
    db = r.app.mongodb
    existing_review = await db[REVIEWS_COLLECTION_NAME].find_one(
        {"$and": [{"plan_id": review.plan_id}, {"user_id": review.user_id}]}
    )
    if existing_review is None:
        review = jsonable_encoder(review)
        new_review = await db[REVIEWS_COLLECTION_NAME].insert_one(review)
        created_review = await db[REVIEWS_COLLECTION_NAME].find_one(
            {"_id": new_review.inserted_id}
        )

        return created_review

    return None


async def get_reviews(
    r: Request, plan_id: str, skip: int, limit: int
) -> ReviewResponse:
    db = r.app.mongodb
    reviews = [
        plan
        async for plan in db[REVIEWS_COLLECTION_NAME].find(
            filter={"plan_id": plan_id}, skip=skip, limit=limit
        )
    ]

    return ReviewResponse(reviews=reviews)


async def get_average_score(r: Request, plan_id: str) -> ReviewAverageScoreResponse:
    db = r.app.mongodb
    pipeline = [
        {"$match": {"plan_id": plan_id}},
        {"$group": {"_id": None, "mean": {"$avg": "$score"}}},
    ]

    cursor = db[REVIEWS_COLLECTION_NAME].aggregate(pipeline)
    current_score = 0
    async for score in cursor:
        current_score = score["mean"]

    return ReviewAverageScoreResponse(mean=current_score)


async def update_review(
    r: Request, review: UpdateReview, review_id: str
) -> UpdateReview | None:
    db = r.app.mongodb
    updated_review = {k: v for k, v in review.dict().items() if v is not None}

    if len(updated_review) > 0:
        result = await db[REVIEWS_COLLECTION_NAME].update_one(
            {"_id": review_id}, {"$set": updated_review}
        )

        if result.modified_count == 1:
            updated_review = await db[TRAININGS_COLLECTION_NAME].find_one(
                {"_id": review_id}
            )

            if updated_review is not None:
                return updated_review

    current_review = await db[REVIEWS_COLLECTION_NAME].find_one({"_id": review_id})

    if current_review is not None:
        return current_review

    return None
