from fastapi import APIRouter, Body, Request
from fastapi.encoders import jsonable_encoder

from app.api.trainers.models import TrainingPlan

router = APIRouter(tags=["plans"])


@router.post("/plans")
async def create_training_plan(plan: TrainingPlan = Body(...)):
    plan = jsonable_encoder(plan)
    new_plan = 



