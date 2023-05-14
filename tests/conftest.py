from pytest import fixture
from starlette.config import environ
from starlette.testclient import TestClient


@fixture(scope="session")
def test_app():
    from app.main import app

    with TestClient(app) as test_client:
        yield test_client


environ["TESTING"] = "TRUE"
