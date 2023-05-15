from pytest import fixture
from starlette.config import environ
from starlette.testclient import TestClient
from app.main import app
from app.config.database import DB_NAME


@fixture
def anyio_backend():
    return "asyncio"


@fixture(scope="session")
def test_app():
    with TestClient(app) as test_client:
        yield test_client


@fixture(autouse=True,scope="session")
def cleanup():
    yield
    app.mongodb.client.drop_database(DB_NAME)


environ["TESTING"] = "TRUE"
