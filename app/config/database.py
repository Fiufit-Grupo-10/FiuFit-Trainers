import os

import motor.motor_asyncio

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")


client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
database = client.trainers


