import os

# import motor.motor_asyncio

MONGO_URL = os.getenv("MONGO_URL", "")
TRAININGS_COLLECTION_NAME = "trainings"
REVIEWS_COLLECTION_NAME = "reviews"
DB_NAME = "trainers_test"


# client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
# database = client.trainers
