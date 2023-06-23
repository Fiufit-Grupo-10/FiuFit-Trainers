from fastapi import FastAPI
from app.api.trainers import routes as trainers_routes
from app.config.database import DB_NAME, MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient
from ddtrace.contrib.asgi import TraceMiddleware
from ddtrace import config

import asyncio

config.fastapi['service_name'] = 'trainings-service'

app = FastAPI()

app.add_middleware(TraceMiddleware)

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(MONGO_URL)
    app.mongodb_client.get_io_loop = asyncio.get_event_loop
    app.mongodb = app.mongodb_client[DB_NAME]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(trainers_routes.router)
