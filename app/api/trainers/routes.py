from fastapi import APIRouter, HTTPException, Request, status, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.status import HTTP_404_NOT_FOUND
from app.config.database import TRAININGS_COLLECTION_NAME
from app.api.trainers.models import (
    BlockTrainingPlan,
    Difficulty,
    TrainingPlan,
    UpdateFavourite,
    UpdateTrainingPlan,
)

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


@router.patch("/plans")
async def block_plan(plans: list[BlockTrainingPlan], request: Request):
    for plan in plans:
        result = await request.app.mongodb[TRAININGS_COLLECTION_NAME].update_one(
            {"_id": plan.uid}, {"$set": {"blocked": plan.blocked}}
        )
        # If it errs some user may be blocked
        if result.modified_count == 0:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=f"Training plan {plan.uid} couldn't be found",
            )


# TODO(@JuanA): Add test
@router.get("/plans/{plan_id}", response_model=TrainingPlan)
async def get_training_plan(plan_id: str, request: Request):
    plan = await request.app.mongodb[TRAININGS_COLLECTION_NAME].find_one(
        {"_id": plan_id}
    )
    if plan is not None:
        return plan

    raise HTTPException(
        status.HTTP_404_NOT_FOUND, detail=f"Plan {plan_id} doesn't exist"
    )


@router.get("/trainers/{trainer_id}/plans", response_model=list[TrainingPlan])
async def get_trainer_training_plans(
    trainer_id: str, request: Request, admin: bool = False
):
    # May break if this is bigger than buffer (skip, limit)
    filters = []
    if not admin:
        filters.append({"blocked": False})

    query = None
    if filters:
        filters.append({"trainer": trainer_id})
        query = {"$and": filters}
    else:
        query = {"trainer": trainer_id}

    return [
        plan
        async for plan in request.app.mongodb[TRAININGS_COLLECTION_NAME].find(query)
    ]


@router.delete("/plans/{trainer_id}/{plan_id}")
async def delete_trainer_plan(plan_id: str, request: Request):
    delete_result = await request.app.mongodb[TRAININGS_COLLECTION_NAME].delete_one(
        {"_id": plan_id}
    )

    if delete_result.deleted_count != 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"plan {plan_id} doesn't exist",
        )

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)


@router.get("/plans", response_model=list[TrainingPlan])
async def get_training_plans(
    request: Request,
    skip: int = 0,
    limit: int = 25,
    admin: bool = False,
    difficulty: Difficulty | None = Query(default=None),
    types: list[str] | None = Query(default=None),
):
    filters = []
    if difficulty is not None:
        filters.append({"difficulty": difficulty})

    if types is not None:
        filters.append({"training_types": {"$all": types}})

    if not admin:
        filters.append({"blocked": False})

    query = None
    if filters:
        query = {"$and": filters}

    return [
        plan
        async for plan in request.app.mongodb[TRAININGS_COLLECTION_NAME].find(
            filter=query, skip=skip, limit=limit
        )
    ]


@router.post("/users/{user_id}/trainings/favourites")
async def add_favourite(user_id: str, favourite: UpdateFavourite, request: Request):
    result = await request.app.mongodb[TRAININGS_COLLECTION_NAME].update_one(
        {"_id": favourite.training_id}, {"$push": {"favourited_by": user_id}}
    )
    if result.modified_count == 1:
        updated_plan = await request.app.mongodb[TRAININGS_COLLECTION_NAME].find_one(
            {"_id": favourite.training_id}
        )
        if updated_plan is not None:
            return

    raise HTTPException(
        status_code=HTTP_404_NOT_FOUND,
        detail=f"Training plan {favourite.training_id} not found",
    )


@router.get("/users/{user_id}/trainings/favourites", response_model=list[TrainingPlan])
async def get_user_favourite_trainings(
    user_id: str,
    request: Request,
    skip: int = 0,
    limit: int = 25,
):
    return [
        plan
        async for plan in request.app.mongodb[TRAININGS_COLLECTION_NAME].find(
            filter={"favourited_by": {"$all": [user_id]}}, skip=skip, limit=limit
        )
    ]


@router.delete("/users/{user_id}/trainings/favourites/{plan_id}")
async def delete_user_favourite_training(user_id: str, plan_id: str, request: Request):
    result = await request.app.mongodb[TRAININGS_COLLECTION_NAME].update_one(
        {"_id": plan_id}, {"$pull": {"favourited_by": user_id}}
    )

    if result.modified_count == 1:
        updated_plan = await request.app.mongodb[TRAININGS_COLLECTION_NAME].find_one(
            {"_id": plan_id}
        )
        if updated_plan is not None:
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)

    raise HTTPException(
        status_code=HTTP_404_NOT_FOUND,
        detail=f"Training plan {plan_id} not found",
    )
