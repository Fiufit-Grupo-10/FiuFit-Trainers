from pytest import fixture
from starlette.config import environ
from starlette.testclient import TestClient
from app.main import app
from app.config.database import (
    DB_NAME,
    REVIEWS_COLLECTION_NAME,
    TRAININGS_COLLECTION_NAME,
)


@fixture
def anyio_backend():
    return "asyncio"


@fixture(scope="session")
def test_app():
    with TestClient(app) as test_client:
        yield test_client


@fixture(autouse=True, scope="function")
async def cleanup():
    yield
    await app.mongodb_client.drop_database(DB_NAME)


environ["TESTING"] = "TRUE"
