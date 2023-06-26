from app.config.database import REVIEWS_COLLECTION_NAME, TRAININGS_COLLECTION_NAME
from app.api.reviews.models import (
    Review,
    UpdateReview,
    ReviewResponse,
    ReviewMeanResponse,
)
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette import status
from app.api.reviews import crud

router = APIRouter(tags=["reviews"])


@router.post("/reviews", response_model=Review | dict)
async def create_review(review: Review, request: Request):
    db = request.app.mongodb
    created_review = await crud.create_review(db, review)
    if created_review is None:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"error": "Review already exists"},
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_review)


@router.put("/reviews/{review_id}", response_model=UpdateReview)
async def update_review(review_id: str, plan: UpdateReview, request: Request):
    updated_review = {k: v for k, v in plan.dict().items() if v is not None}

    if len(updated_review) > 0:
        result = await request.app.mongodb[REVIEWS_COLLECTION_NAME].update_one(
            {"_id": review_id}, {"$set": updated_review}
        )

        if result.modified_count == 1:
            updated_review = await request.app.mongodb[
                TRAININGS_COLLECTION_NAME
            ].find_one({"_id": review_id})

            if updated_review is not None:
                return updated_review

    current_review = await request.app.mongodb[REVIEWS_COLLECTION_NAME].find_one(
        {"_id": review_id}
    )

    if current_review is not None:
        return current_review

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Review {review_id} not found"
    )


@router.get("/reviews/{plan_id}/mean", response_model=ReviewMeanResponse)
async def get_plan_average_score(
    plan_id: str,
    request: Request,
):
    pipeline = [
        {"$match": {"plan_id": plan_id}},
        {"$group": {"_id": None, "mean": {"$avg": "$score"}}},
    ]
    cursor = request.app.mongodb[REVIEWS_COLLECTION_NAME].aggregate(pipeline)

    current_score = 0
    async for score in cursor:
        current_score = score["mean"]

    return JSONResponse(status_code=status.HTTP_200_OK, content={"mean": current_score})


@router.get("/reviews/{plan_id}", response_model=ReviewResponse)
async def get_training_plan_reviews(
    plan_id: str,
    request: Request,
    skip: int = 0,
    limit: int = 25,
):
    reviews = [
        plan
        async for plan in request.app.mongodb[REVIEWS_COLLECTION_NAME].find(
            filter={"plan_id": plan_id}, skip=skip, limit=limit
        )
    ]
    content = {"reviews": reviews}
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)
