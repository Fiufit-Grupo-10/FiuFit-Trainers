from fastapi import FastAPI
from app.api.trainers import routes as trainers_routes

app = FastAPI()


app.include_router(trainers_routes.router)

