from fastapi import APIRouter, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.status import HTTP_404_NOT_FOUND
from app.config.database import COLLECTION_NAME
from app.api.trainers.models import TrainingPlan, UpdateTrainingPlan

router = APIRouter(tags=["plans"])


@router.post("/plans", response_model=TrainingPlan)
async def create_training_plan(plan: TrainingPlan, request: Request):
    plan = jsonable_encoder(plan)
    new_plan = await request.app.mongodb[COLLECTION_NAME].insert_one(plan)
    created_plan = await request.app.mongodb[COLLECTION_NAME].find_one(
        {"_id": new_plan.inserted_id}
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_plan)


# TODO: Does it make sense to make it idempotent
@router.put("/plans/{id}", response_model=TrainingPlan)
async def modify_training_plan(id: str, plan: UpdateTrainingPlan, request: Request):
    updated_plan = {k: v for k, v in plan.dict().items() if v is not None}

    if len(updated_plan) > 0:
        result = await request.app.mongodb[COLLECTION_NAME].update_one(
            {"_id": id}, {"$set": updated_plan}
        )

        if result.modified_count == 1:
            updated_plan = await request.app.mongodb[COLLECTION_NAME].find_one(
                {"_id": id}
            )
            if updated_plan is not None:
                return updated_plan

    current_plan = await request.app.mongodb[COLLECTION_NAME].find_one({"_id": id})
    if current_plan is not None:
        return current_plan

    raise HTTPException(
        status_code=HTTP_404_NOT_FOUND, detail=f"Training plan {id} not found"
    )


@router.get("/plans/{trainer_id}", response_model=list[TrainingPlan])
async def get_training_plans(trainer_id: str, request: Request):
    # May break if this is bigger than buffer
    return [
        plan
        async for plan in request.app.mongodb[COLLECTION_NAME].find(
            {"trainer": trainer_id}
        )
    ]
