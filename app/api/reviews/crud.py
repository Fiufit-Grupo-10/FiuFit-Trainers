from app.api.reviews.models import Review
from app.config.database import REVIEWS_COLLECTION_NAME
from fastapi.encoders import jsonable_encoder

async def create_review(db, review: Review) -> Review | None:
    existing_review = await db[REVIEWS_COLLECTION_NAME].find_one(
        {"$and": [{"plan_id": review.plan_id}, {"user_id": review.user_id}]}
    )
    if existing_review is None:
        review = jsonable_encoder(review)
        new_review = await db[REVIEWS_COLLECTION_NAME].insert_one(
            review
        )
        created_review = await db[REVIEWS_COLLECTION_NAME].find_one(
            {"_id": new_review.inserted_id}
        )

        return created_review
        
    return None
