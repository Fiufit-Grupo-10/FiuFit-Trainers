from starlette.status import HTTP_409_CONFLICT
import pytest


@pytest.mark.anyio
async def test_create_review(test_app):
    review = {
        "plan_id": "c59710ef-f5d0-41ba-a787-ad8eb739ef4c",
        "user_id": "7ca0fa95-af47-40b4-8e39-2fae5ee2667a",
        "review": "Very good training",
        "score": 2,
    }
    response = test_app.post("/reviews", json=review)
    assert response.status_code == 201

    body = response.json()
    assert "_id" in body


@pytest.mark.anyio
async def test_try_to_create_two_reviews_for_the_same_plan(test_app):
    review = {
        "plan_id": "c59710ef-f5d0-41ba-a787-ad8eb739ef4c",
        "user_id": "7ca0fa95-af47-40b4-8e39-2fae5ee2667a",
        "review": "Very good training",
        "score": 2,
    }
    response = test_app.post("/reviews", json=review)
    assert response.status_code == 201

    review = {
        "plan_id": "c59710ef-f5d0-41ba-a787-ad8eb739ef4c",
        "user_id": "7ca0fa95-af47-40b4-8e39-2fae5ee2667a",
        "review": "New review, Very good training",
        "score": 3,
    }
    response = test_app.post("/reviews", json=review)
    assert response.status_code == HTTP_409_CONFLICT


@pytest.mark.anyio
async def test_create_review_with_invalid_score(test_app):
    review_1 = {
        "plan_id": "c59710ef-f5d0-41ba-a787-ad8eb739ef4c",
        "user_id": "7ca0fa95-af47-40b4-8e39-2fae5ee2667a",
        "review": "Very good training",
        "score": 10,
    }

    review_2 = {
        "plan_id": "c59710ef-f5d0-41ba-a787-ad8eb739ef4c",
        "user_id": "7ca0fa95-af47-40b4-8e39-2fae5ee2667a",
        "review": "Very good training",
        "score": -2,
    }

    response = test_app.post("/reviews", json=review_1)
    assert response.status_code == 422

    response = test_app.post("/reviews", json=review_2)
    assert response.status_code == 422
