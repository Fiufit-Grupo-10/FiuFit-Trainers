from typing import Tuple
from fastapi import Request, HTTPException
from starlette import status
from fastapi.encoders import jsonable_encoder
from app.config.database import TRAININGS_COLLECTION_NAME
from app.api.trainers.models import (
    BlockTrainingPlan,
    Difficulty,
    TrainingPlan,
    UpdateFavourite,
    UpdateTrainingPlan,
)


async def create_plan(r: Request, plan: TrainingPlan) -> TrainingPlan:
    db = r.app.mongodb
    plan = jsonable_encoder(plan)
    new_plan = await db[TRAININGS_COLLECTION_NAME].insert_one(plan)
    created_plan = await db[TRAININGS_COLLECTION_NAME].find_one(
        {"_id": new_plan.inserted_id}
    )
    return created_plan


async def update_plan(
    r: Request, plan: UpdateTrainingPlan, plan_id: str
) -> TrainingPlan | None:
    db = r.app.mongodb
    updated_plan = {k: v for k, v in plan.dict().items() if v is not None}
    if len(updated_plan) > 0:
        result = await db[TRAININGS_COLLECTION_NAME].update_one(
            {"_id": plan_id}, {"$set": updated_plan}
        )

        if result.modified_count == 1:
            updated_plan = await db[TRAININGS_COLLECTION_NAME].find_one(
                {"_id": plan_id}
            )
            if updated_plan is not None:
                return updated_plan

    current_plan = await db[TRAININGS_COLLECTION_NAME].find_one({"_id": plan_id})
    if current_plan is not None:
        return current_plan

    return None


async def block_plan(r: Request, plans: list[BlockTrainingPlan]) -> Tuple[str, bool]:
    db = r.app.mongodb
    for plan in plans:
        result = await db[TRAININGS_COLLECTION_NAME].update_one(
            {"_id": plan.uid}, {"$set": {"blocked": plan.blocked}}
        )
        # If it errs some user may be blocked
        if result.modified_count == 0:
            return (plan.uid, False)
    return ("", True)


async def get_plan(r: Request, plan_id: str) -> TrainingPlan | None:
    db = r.app.mongodb
    plan = await db[TRAININGS_COLLECTION_NAME].find_one({"_id": plan_id})
    return plan


async def get_trainer_plans(
    r: Request, trainer_id: str, admin: bool
) -> list[TrainingPlan]:
    db = r.app.mongodb
    filters = []
    if not admin:
        filters.append({"blocked": False})

    query = None
    if filters:
        filters.append({"trainer": trainer_id})
        query = {"$and": filters}
    else:
        query = {"trainer": trainer_id}

    return [plan async for plan in db[TRAININGS_COLLECTION_NAME].find(query)]


async def get_user_favourite_plans(
    r: Request,
    user_id: str,
    skip: int,
    limit: int,
):
    db = r.app.mongodb
    return [
        plan
        async for plan in db[TRAININGS_COLLECTION_NAME].find(
            filter={"favourited_by": {"$all": [user_id]}}, skip=skip, limit=limit
        )
    ]

async def delete_user_favourite_plan(r: Request, user_id: str, plan_id: str) -> bool:
    db = r.app.mongodb
    result = await db[TRAININGS_COLLECTION_NAME].update_one(
        {"_id": plan_id}, {"$pull": {"favourited_by": user_id}}
    )

    if result.modified_count == 1:
        updated_plan = await db[TRAININGS_COLLECTION_NAME].find_one(
            {"_id": plan_id}
        )
        if updated_plan is not None:
            return True
    return False


async def add_favourite(r: Request, user_id: str, favourite: UpdateFavourite) -> bool:
    db = r.app.mongodb
    result = await db[TRAININGS_COLLECTION_NAME].update_one(
        {"_id": favourite.training_id}, {"$addToSet": {"favourited_by": user_id}}
    )
    if result.modified_count == 1:
        updated_plan = await db[TRAININGS_COLLECTION_NAME].find_one(
            {"_id": favourite.training_id}
        )
        if updated_plan is not None:
            return True

    return False


async def delete_plan(r: Request, plan_id: str) -> bool:
    db = r.app.mongodb
    delete_result = await db[TRAININGS_COLLECTION_NAME].delete_one(
        {"_id": plan_id}
    )

    if delete_result.deleted_count != 1:
        return False

    return True


async def get_plans(
    r: Request,
    skip: int,
    limit: int,
    admin: bool,
    difficulty: Difficulty | None,
    types: list[str] | None,
) -> list[TrainingPlan]:
    db = r.app.mongodb
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
        async for plan in db[TRAININGS_COLLECTION_NAME].find(
            filter=query, skip=skip, limit=limit
        )
    ]
