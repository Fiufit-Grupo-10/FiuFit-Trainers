from fastapi import APIRouter, HTTPException, Request, status, Query
from fastapi.responses import JSONResponse
from starlette.status import HTTP_404_NOT_FOUND
from app.api.trainers import crud
from app.api.trainers.models import (
    BlockTrainingPlan,
    Difficulty,
    TrainingPlan,
    UpdateFavourite,
    UpdateTrainingPlan,
)
from app.config import config
from app.api.metrics.service import MetricsService, get_metrics
from app.config.config import logger


router = APIRouter(tags=["plans"])


@router.post("/plans", response_model=TrainingPlan)
async def create_plan(plan: TrainingPlan, request: Request):
    created_plan = await crud.create_plan(request, plan)
    logger.info("creating training plan", id=plan.id, trainer=plan.trainer)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_plan)


@router.put("/plans/{plan_id}", response_model=TrainingPlan)
async def update_plan(plan_id: str, plan: UpdateTrainingPlan, request: Request):
    logger.info("updating training plan", id=plan_id)
    updated_plan = await crud.update_plan(request, plan, plan_id)
    if updated_plan is not None:
        logger.info("updated training plan", id=plan_id)
        return updated_plan

    logger.info("failed to update plan", id=plan_id, error="not found")
    raise HTTPException(
        status_code=HTTP_404_NOT_FOUND, detail=f"Training plan {plan_id} not found"
    )


@router.patch("/plans")
async def block_plan(plans: list[BlockTrainingPlan], request: Request):
    plan_id, ok = await crud.block_plan(request, plans)
    # If it errs some user may be blocked
    if not ok:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Training plan {plan_id} couldn't be found",
        )


@router.get("/plans/{plan_id}", response_model=TrainingPlan)
async def get_plan(plan_id: str, request: Request):
    plan = await crud.get_plan(request, plan_id)

    if plan is not None:
        return plan

    raise HTTPException(
        status.HTTP_404_NOT_FOUND, detail=f"Plan {plan_id} doesn't exist"
    )


@router.get("/trainers/{trainer_id}/plans", response_model=list[TrainingPlan])
async def get_trainer_training_plans(
    trainer_id: str, request: Request, admin: bool = False
):
    return await crud.get_trainer_plans(request, trainer_id, admin)


@router.delete("/plans/{trainer_id}/{plan_id}")
async def delete_plan(plan_id: str, request: Request):
    deleted = await crud.delete_plan(request, plan_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"plan {plan_id} doesn't exist",
        )

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)


@router.get("/plans", response_model=list[TrainingPlan])
async def get_plans(
    request: Request,
    skip: int = 0,
    limit: int = 25,
    admin: bool = False,
    difficulty: Difficulty | None = Query(default=None),
    types: list[str] | None = Query(default=None),
):
    return await crud.get_plans(request, skip, limit, admin, difficulty, types)


@router.post("/users/{user_id}/trainings/favourites")
async def add_favourite(user_id: str, favourite: UpdateFavourite, request: Request):
    ok = await crud.add_favourite(request, user_id, favourite)
    if not ok:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Training plan {favourite.training_id} not found",
        )
    logger.info("Added favourite", user=user_id, plan=favourite.training_id)
    if config.METRICS_URL is not None:
        metrics = await get_metrics(request, favourite.training_id)
        if metrics is not None:
            await MetricsService(metrics).send()


@router.get("/users/{user_id}/trainings/favourites", response_model=list[TrainingPlan])
async def get_user_favourite_plans(
    user_id: str,
    request: Request,
    skip: int = 0,
    limit: int = 25,
):
    return await crud.get_user_favourite_plans(request, user_id, skip, limit)


@router.delete(
    "/users/{user_id}/trainings/favourites/{plan_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user_favourite_plan(user_id: str, plan_id: str, request: Request):
    deleted = await crud.delete_user_favourite_plan(request, user_id, plan_id)
    if not deleted:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Training plan {plan_id} not found",
        )
    logger.info("Deleted favourite", user=user_id, plan=plan_id)
    if config.METRICS_URL is not None:
        metrics = await get_metrics(request, plan_id)
        if metrics is not None:
            await MetricsService(metrics).send()
