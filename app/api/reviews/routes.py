from app.api.metrics.service import MetricsService, get_metrics
from app.api.reviews.models import (
    Review,
    UpdateReview,
    ReviewResponse,
    ReviewAverageScoreResponse,
)
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import JSONResponse
from app.api.reviews import crud
from app.config import config
from app.config.config import logger

router = APIRouter(tags=["reviews"])


@router.post("/reviews", response_model=Review | dict)
async def create_review(review: Review, request: Request):
    created_review = await crud.create_review(request, review)
    if created_review is None:
        logger.info("review already exist", plan=review.plan_id, user=review.user_id)
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"error": "Review already exists"},
        )
    logger.info("created review", plan=review.plan_id, user=review.user_id)
    if config.METRICS_URL is not None:
        metrics = await get_metrics(request, review.plan_id)
        if metrics is not None:
            await MetricsService(metrics).send()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_review)


@router.put("/reviews/{review_id}", response_model=Review)
async def update_review(review_id: str, review: UpdateReview, request: Request):
    response = await crud.update_review(request, review, review_id)
    logger.info("updating review", review=review_id)
    if response is not None:
        logger.info("review updated", review=review_id)
        if config.METRICS_URL is not None:
            metrics = await get_metrics(request, response.plan_id)
            if metrics is not None:
                await MetricsService(metrics).send()
        return response

    logger.info("failed to update review", review=review_id)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Review {review_id} not found"
    )


@router.get("/reviews/{plan_id}/mean", response_model=ReviewAverageScoreResponse)
async def get_plan_average_score(
    plan_id: str,
    request: Request,
):
    return await crud.get_average_score(request, plan_id)


@router.get("/reviews/{plan_id}", response_model=ReviewResponse)
async def get_training_plan_reviews(
    plan_id: str,
    request: Request,
    skip: int = 0,
    limit: int = 25,
):
    content = await crud.get_reviews(request, plan_id, skip, limit)
    return content
