from fastapi import APIRouter, Body, Request,status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.api.trainers.models import TrainingPlan

router = APIRouter(tags=["plans"])


@router.post("/plans",response_model=TrainingPlan)
async def create_training_plan(plan: TrainingPlan,request: Request):
    plan = jsonable_encoder(plan)
    new_plan = await request.app.mongodb["trainers"].insert_one(plan)
    created_plan = await request.app.mongodb["trainers"].find_one({"_id": new_plan.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_plan)  