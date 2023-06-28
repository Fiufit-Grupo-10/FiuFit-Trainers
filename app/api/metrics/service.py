from fastapi import Request
from fastapi.encoders import jsonable_encoder
from app.config.config import METRICS_URL
from app.config.database import REVIEWS_COLLECTION_NAME, TRAININGS_COLLECTION_NAME
from pydantic import BaseModel, Field
import httpx


class Metrics(BaseModel):
    plan_id: str = Field(...)
    metric: str = Field(default="score")
    favourite_counter: int = Field(default=0)
    review_counter: int = Field(default=0)
    review_average: float = Field(default=0.0)


class MetricsService:
    metrics: Metrics

    def __init__(self, metrics: Metrics):
        self.metrics = metrics

    async def send(self):
        url = f"{METRICS_URL}/metrics/trainings/{self.metrics.plan_id}"
        async with httpx.AsyncClient() as client:
            # TODO: Log
            await client.put(url, json=jsonable_encoder(self.metrics))


async def get_metrics(r: Request, plan_id: str) -> Metrics | None:
    db = r.app.mongodb
    pipeline = [
        {"$match": {"plan_id": plan_id}},
        {
            "$group": {
                "_id": None,
                "mean": {"$avg": "$score"},
                "count": {"$count": "reviews"},
            }
        },
    ]
    reviews_cursor = db[REVIEWS_COLLECTION_NAME].aggregate(pipeline)
    reviews_counter = 0
    review_average = 0.0
    async for review in reviews_cursor:
        reviews_counter = review["count"]["reviews"]
        review_average = review["mean"]

    plan = await db.mongodb[TRAININGS_COLLECTION_NAME].find_one({"_id": plan_id})
    if plan is None:
        return None

    favourite_counter = len(plan["favourited_by"])
    return Metrics(
        plan_id=plan_id,
        favourite_counter=favourite_counter,
        review_counter=reviews_counter,
        review_average=review_average,
    )
