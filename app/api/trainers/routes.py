from fastapi import APIRouter, HTTPException, Request, status, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.status import HTTP_404_NOT_FOUND
from app.config.database import TRAININGS_COLLECTION_NAME, REVIEWS_COLLECTION_NAME
from app.api.trainers.models import (
    Review,
    ReviewResponse,
    TrainingPlan,
    UpdateTrainingPlan,
)
import statistics

router = APIRouter(tags=["plans"])


@router.post("/plans", response_model=TrainingPlan)
async def create_training_plan(plan: TrainingPlan, request: Request):
    plan = jsonable_encoder(plan)
    new_plan = await request.app.mongodb[TRAININGS_COLLECTION_NAME].insert_one(plan)
    created_plan = await request.app.mongodb[TRAININGS_COLLECTION_NAME].find_one(
        {"_id": new_plan.inserted_id}
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_plan)


@router.put("/plans/{plan_id}", response_model=TrainingPlan)
async def modify_training_plan(
    plan_id: str, plan: UpdateTrainingPlan, request: Request
):
    updated_plan = {k: v for k, v in plan.dict().items() if v is not None}

    if len(updated_plan) > 0:
        result = await request.app.mongodb[TRAININGS_COLLECTION_NAME].update_one(
            {"_id": plan_id}, {"$set": updated_plan}
        )

        if result.modified_count == 1:
            updated_plan = await request.app.mongodb[
                TRAININGS_COLLECTION_NAME
            ].find_one({"_id": plan_id})
            if updated_plan is not None:
                return updated_plan

    current_plan = await request.app.mongodb[TRAININGS_COLLECTION_NAME].find_one(
        {"_id": plan_id}
    )
    if current_plan is not None:
        return current_plan

    raise HTTPException(
        status_code=HTTP_404_NOT_FOUND, detail=f"Training plan {plan_id} not found"
    )


@router.get("/plans/{trainer_id}", response_model=list[TrainingPlan])
async def get_trainer_training_plans(trainer_id: str, request: Request):
    # May break if this is bigger than buffer
    return [
        plan
        async for plan in request.app.mongodb[TRAININGS_COLLECTION_NAME].find(
            {"trainer": trainer_id}
        )
    ]


@router.get("/plans")
async def get_training_plans(
    request: Request,
    skip: int = 0,
    limit: int = 25,
    types: list[str] | None = Query(default=None),
):
    query = None
    if types is not None:
        query = {"training_types": {"$all": types}}

    return [
        plan
        async for plan in request.app.mongodb[TRAININGS_COLLECTION_NAME].find(
            filter=query, skip=skip, limit=limit
        )
    ]


@router.post("/reviews", response_model=Review)
async def create_review(review: Review, request: Request):
    review = jsonable_encoder(review)
    new_review = await request.app.mongodb[REVIEWS_COLLECTION_NAME].insert_one(review)
    created_review = await request.app.mongodb[REVIEWS_COLLECTION_NAME].find_one(
        {"_id": new_review.inserted_id}
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_review)


@router.get("/reviews/{plan_id}", response_model=ReviewResponse)
async def get_training_plan_reviews(plan_id: str, request: Request):
    # May break if this is bigger than buffer
    reviews = [
        plan
        async for plan in request.app.mongodb[REVIEWS_COLLECTION_NAME].find(
            {"plan_id": plan_id}
        )
    ]
    
    scores = [r["score"] for r in reviews]
    content = {}
    if reviews
        mean = statistics.fmean(scores)
        content = {"reviews": reviews, "mean": mean}
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)
