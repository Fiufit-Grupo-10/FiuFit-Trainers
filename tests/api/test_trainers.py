from app.api.trainers import routes
from app.config.database import TRAININGS_COLLECTION_NAME
from app.main import app
from starlette import status
from httpx import AsyncClient
import pytest


def test_create_plan_without_errors(test_app):
    plan = {
        "trainer": "c59710ef-f5d0-41ba-a787-ad8eb739ef4c",
        "title": "Sample training plan",
        "description": "Training plan description",
        "difficulty": "beginner",
        "training_types": ["cardio"],
        "goals": ["plank: one minute"],
        "duration": 90,
        "reviews": None,
    }

    response = test_app.post("/plans", json=plan)
    assert response.status_code == 201

    body = response.json()
    assert "_id" in body


def test_plan_with_missing_field(test_app):
    plan = {
        "title": "Sample training plan",
        "description": "Training plan description",
        "difficulty": "beginner",
        "training_types": ["cardio"],
        "goals": ["plank: one minute"],
        "duration": 90,
        "reviews": None,
    }
    response = test_app.post("/plans", json=plan)
    assert response.status_code == 422


@pytest.mark.anyio
async def test_update_existing_plan():
    plan = {
        "trainer": "c59710ef-f5d0-41ba-a787-ad8eb739ef4c",
        "title": "Sample training plan",
        "description": "Training plan description",
        "difficulty": "beginner",
        "training_types": ["cardio"],
        "goals": ["plank: one minute"],
        "duration": 90,
        "reviews": None,
        "favourited_by": [],
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/plans", json=plan)

    id = response.json()["_id"]

    updated_plan = {
        "title": "Updated training plan",
        "description": "Updated plan description",
        "difficulty": "advanced",
        "training_types": ["cardio", "hiit"],
        "goals": ["plank: two minute"],
        "duration": 30,
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put(f"/plans/{id}", json=updated_plan)

    assert response.status_code == 200
    async with AsyncClient(app=app, base_url="http://test") as ac:
        current_plan = await app.mongodb[TRAININGS_COLLECTION_NAME].find_one(
            {"_id": id}
        )

    expected_plan = {
        "_id": id,
        "trainer": "c59710ef-f5d0-41ba-a787-ad8eb739ef4c",
        "title": "Updated training plan",
        "description": "Updated plan description",
        "difficulty": "advanced",
        "training_types": ["cardio", "hiit"],
        "goals": ["plank: two minute"],
        "duration": 30,
        "blocked": False,
        "favourited_by": [],
    }

    assert current_plan == expected_plan


@pytest.mark.anyio
async def test_update_with_empty_body():
    plan = {
        "trainer": "c59710ef-f5d0-41ba-a787-ad8eb739ef4c",
        "title": "Sample training plan",
        "description": "Training plan description",
        "difficulty": "beginner",
        "training_types": ["cardio"],
        "goals": ["plank: one minute"],
        "duration": 90,
        "blocked": False,
        "favourited_by": [],
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/plans", json=plan)

    id = response.json()["_id"]

    updated_plan = {}

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put(f"/plans/{id}", json=updated_plan)

    assert response.status_code == 200

    async with AsyncClient(app=app, base_url="http://test") as ac:
        current_plan = await app.mongodb[TRAININGS_COLLECTION_NAME].find_one(
            {"_id": id}
        )

    expected_plan = {
        "_id": id,
        "trainer": "c59710ef-f5d0-41ba-a787-ad8eb739ef4c",
        "title": "Sample training plan",
        "description": "Training plan description",
        "difficulty": "beginner",
        "training_types": ["cardio"],
        "goals": ["plank: one minute"],
        "duration": 90,
        "blocked": False,
        "favourited_by": [],
    }

    assert current_plan == expected_plan


def test_update_unexisting_plan(test_app):
    updated_plan = {
        "trainer": "c59710ef-f5d0-41ba-a787-ad8eb739ef4c",
        "title": "Sample training plan",
        "description": "Training plan description",
        "difficulty": "beginner",
        "training_types": ["cardio"],
        "goals": ["plank: one minute"],
        "duration": 90,
        "reviews": None,
    }
    id = "unexisting_id"

    response = test_app.put(f"/plans/{id}", json=updated_plan)

    assert response.status_code == 404


@pytest.mark.anyio
async def test_delete_existing_plan():
    plan = {
        "trainer": "c59710ef-f5d0-41ba-a787-ad8eb739ef4c",
        "title": "Sample training plan",
        "description": "Training plan description",
        "difficulty": "beginner",
        "training_types": ["cardio"],
        "media": ["link-to-image", "link-to-video"],
        "goals": ["plank: one minute"],
        "duration": 90,
        "reviews": None,
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/plans", json=plan)

    id = response.json()["_id"]

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(f"/plans/c59710ef-f5d0-41ba-a787-ad8eb739ef4c/{id}")

    assert response.status_code == 204


@pytest.mark.anyio
async def test_delete_non_existing_plan():
    id = "abc"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(f"/plans/xyz/{id}")

    assert response.status_code == 404


@pytest.mark.anyio
async def test_obtain_created_plans_of_certain_trainer():
    trainer = "Abdulazeez trainer"
    plan_1 = {
        "trainer": trainer,
        "title": "Pilates training plan",
        "description": "A pilates training plan",
        "difficulty": "beginner",
        "training_types": ["cardio"],
        "goals": ["plank: one minute"],
        "duration": 30,
        "reviews": None,
        "blocked": False,
        "favourited_by": [],
    }

    plan_2 = {
        "trainer": trainer,
        "title": "Crossfit training plan",
        "description": "A crossfit training plan",
        "difficulty": "beginner",
        "training_types": ["cardio"],
        "goals": ["plank: one minute"],
        "duration": 120,
        "reviews": None,
        "blocked": False,
        "favourited_by": [],
    }

    plan_1_ = {
        "_id": "",
        "trainer": trainer,
        "title": "Pilates training plan",
        "description": "A pilates training plan",
        "difficulty": "beginner",
        "training_types": ["cardio"],
        "goals": ["plank: one minute"],
        "duration": 30,
        "blocked": False,
        "favourited_by": [],
    }

    plan_2_ = {
        "_id": "",
        "trainer": trainer,
        "title": "Crossfit training plan",
        "description": "A crossfit training plan",
        "difficulty": "beginner",
        "training_types": ["cardio"],
        "goals": ["plank: one minute"],
        "duration": 120,
        "blocked": False,
        "favourited_by": [],
    }
    expected = [plan_1_, plan_2_]

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response_1 = await ac.post("/plans", json=plan_1)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response_2 = await ac.post("/plans", json=plan_2)

    assert response_1.status_code == 201
    assert response_2.status_code == 201

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response_3 = await ac.get(f"/trainers/{trainer}/plans")

    json_result = response_3.json()

    assert len(json_result) == 2

    assert json_result[0] != json_result[1]

    json_result[0]["_id"] = ""
    json_result[1]["_id"] = ""

    assert (json_result[0] == expected[0]) or (json_result[0] == expected[1])
    assert (json_result[1] == expected[0]) or (json_result[1] == expected[1])


@pytest.mark.anyio
async def test_get_trainer_plans_when_some_are_blocked():
    trainer = "Abdulazeez trainer"
    plans = [
        {
            "trainer": trainer,
            "title": "Pilates training plan",
            "description": "A pilates training plan",
            "difficulty": "beginner",
            "training_types": ["cardio"],
            "media": ["link-to-image", "link-to-video"],
            "goals": ["plank: one minute"],
            "duration": 30,
            "reviews": None,
            "blocked": True,
        },
        {
            "trainer": trainer,
            "title": "Crossfit training plan",
            "description": "A crossfit training plan",
            "difficulty": "intermediate",
            "training_types": ["cardio"],
            "media": ["link-to-image", "link-to-video"],
            "goals": ["plank: one minute"],
            "duration": 120,
            "reviews": None,
            "blocked": True,
        },
        {
            "trainer": trainer,
            "title": "Pilates training plan",
            "description": "A pilates training plan",
            "difficulty": "beginner",
            "training_types": ["cardio"],
            "media": ["link-to-image", "link-to-video"],
            "goals": ["plank: one minute"],
            "duration": 30,
            "blocked": True,
        },
        {
            "trainer": trainer,
            "title": "Crossfit training plan",
            "description": "A crossfit training plan",
            "difficulty": "beginner",
            "training_types": ["cardio"],
            "media": ["link-to-image", "link-to-video"],
            "goals": ["plank: one minute"],
            "duration": 120,
            "blocked": False,
        },
    ]

    trainer_id = None
    for plan in plans:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/plans", json=plan)
            trainer_id = response.json()["trainer"]

    params = {"admin": False}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/trainers/{trainer_id}/plans", params=params)

    json_result = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(json_result) == 1

    params = {"admin": True}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/trainers/{trainer_id}/plans", params=params)

    json_result = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(json_result) == 4


def test_create_review_without_errors(test_app):
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


def test_create_review_with_invalid_score(test_app):
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


def test_obtain_n_plans(test_app):
    plan = {
        "trainer": "Abdulazeez trainer",
        "title": "Pilates training plan",
        "description": "A pilates training plan",
        "difficulty": "beginner",
        "training_types": ["cardio"],
        "media": ["link-to-image", "link-to-video"],
        "goals": ["plank: one minute"],
        "duration": 30,
        "reviews": None,
    }
    response = test_app.post("/plans", json=plan)
    id = response.json()["_id"]

    review_1 = {
        "plan_id": id,
        "user_id": "7ca0fa95-af47-40b4-8e39-2fae5ee2667a",
        "review": "1",
        "score": 2,
    }
    review_2 = {
        "plan_id": id,
        "user_id": "7ca0fa95asffffffffffffads",
        "review": "2",
        "score": 2,
    }
    review_3 = {
        "plan_id": id,
        "user_id": "7ca0fa95-afasdddddddddd",
        "review": "3",
        "score": 5,
    }
    review_4 = {
        "plan_id": id,
        "user_id": "7ca0fa95-af47-40b4-8e39-2fae5ee2667a",
        "review": "4",
        "score": 5,
    }
    response_1 = test_app.post("/reviews", json=review_1)
    response_2 = test_app.post("/reviews", json=review_2)
    response_3 = test_app.post("/reviews", json=review_3)
    response_4 = test_app.post("/reviews", json=review_4)

    result1 = test_app.get(f"/reviews/{id}/mean")
    result = test_app.get(f"/reviews/{id}", params={"limit": "1", "skip": "1"})


@pytest.mark.anyio
async def test_search_training_plan_by_difficulty():
    trainer = "Abdulazeez trainer"
    plans = [
        {
            "trainer": trainer,
            "title": "Pilates training plan",
            "description": "A pilates training plan",
            "difficulty": "beginner",
            "training_types": ["cardio"],
            "media": ["link-to-image", "link-to-video"],
            "goals": ["plank: one minute"],
            "duration": 30,
            "reviews": None,
        },
        {
            "trainer": trainer,
            "title": "Crossfit training plan",
            "description": "A crossfit training plan",
            "difficulty": "intermediate",
            "training_types": ["cardio"],
            "media": ["link-to-image", "link-to-video"],
            "goals": ["plank: one minute"],
            "duration": 120,
            "reviews": None,
        },
        {
            "trainer": trainer,
            "title": "Pilates training plan",
            "description": "A pilates training plan",
            "difficulty": "beginner",
            "training_types": ["cardio"],
            "media": ["link-to-image", "link-to-video"],
            "goals": ["plank: one minute"],
            "duration": 30,
        },
        {
            "trainer": trainer,
            "title": "Crossfit training plan",
            "description": "A crossfit training plan",
            "difficulty": "beginner",
            "training_types": ["cardio"],
            "media": ["link-to-image", "link-to-video"],
            "goals": ["plank: one minute"],
            "duration": 120,
        },
    ]

    for plan in plans:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/plans", json=plan)

    params = {"difficulty": "beginner"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/plans", params=params)

    json_result = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(json_result) == 3

    params = {"difficulty": "advanced"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/plans", params=params)

    json_result = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(json_result) == 0


@pytest.mark.anyio
async def test_search_training_plans_when_users_are_blocked():
    trainer = "Abdulazeez trainer"
    plans = [
        {
            "trainer": trainer,
            "title": "Pilates training plan",
            "description": "A pilates training plan",
            "difficulty": "beginner",
            "training_types": ["cardio"],
            "media": ["link-to-image", "link-to-video"],
            "goals": ["plank: one minute"],
            "duration": 30,
            "reviews": None,
            "blocked": True,
        },
        {
            "trainer": trainer,
            "title": "Crossfit training plan",
            "description": "A crossfit training plan",
            "difficulty": "intermediate",
            "training_types": ["cardio"],
            "media": ["link-to-image", "link-to-video"],
            "goals": ["plank: one minute"],
            "duration": 120,
            "reviews": None,
        },
        {
            "trainer": trainer,
            "title": "Pilates training plan",
            "description": "A pilates training plan",
            "difficulty": "beginner",
            "training_types": ["cardio"],
            "media": ["link-to-image", "link-to-video"],
            "goals": ["plank: one minute"],
            "duration": 30,
        },
        {
            "trainer": trainer,
            "title": "Crossfit training plan",
            "description": "A crossfit training plan",
            "difficulty": "beginner",
            "training_types": ["cardio"],
            "media": ["link-to-image", "link-to-video"],
            "goals": ["plank: one minute"],
            "duration": 120,
        },
    ]

    for plan in plans:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/plans", json=plan)

    params = {"admin": False}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/plans", params=params)

    json_result = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(json_result) == 3

    params = {"admin": True}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/plans", params=params)

    json_result = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(json_result) == 4


@pytest.mark.anyio
async def test_search_training_plan():
    trainer = "Abdulazeez trainer"
    plans = [
        {
            "trainer": trainer,
            "title": "Pilates training plan",
            "description": "A pilates training plan",
            "difficulty": "beginner",
            "training_types": ["cardio"],
            "media": ["link-to-image", "link-to-video"],
            "goals": ["plank: one minute"],
            "duration": 30,
            "reviews": None,
        },
        {
            "trainer": trainer,
            "title": "Crossfit training plan",
            "description": "A crossfit training plan",
            "difficulty": "intermediate",
            "training_types": ["cardio"],
            "media": ["link-to-image", "link-to-video"],
            "goals": ["plank: one minute"],
            "duration": 120,
            "reviews": None,
        },
        {
            "trainer": trainer,
            "title": "Pilates training plan",
            "description": "A pilates training plan",
            "difficulty": "beginner",
            "training_types": ["cardio"],
            "media": ["link-to-image", "link-to-video"],
            "goals": ["plank: one minute"],
            "duration": 30,
        },
        {
            "trainer": trainer,
            "title": "Crossfit training plan",
            "description": "A crossfit training plan",
            "difficulty": "beginner",
            "training_types": ["cardio"],
            "media": ["link-to-image", "link-to-video"],
            "goals": ["plank: one minute"],
            "duration": 120,
        },
    ]

    for plan in plans:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/plans", json=plan)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/plans")

    json_result = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(json_result) == 4


@pytest.mark.anyio
async def test_block_user():
    plan = {
        "trainer": "Abdulazeez trainer",
        "title": "Pilates training plan",
        "description": "A pilates training plan",
        "difficulty": "beginner",
        "training_types": ["cardio"],
        "media": ["link-to-image", "link-to-video"],
        "goals": ["plank: one minute"],
        "duration": 30,
        "reviews": None,
        "blocked": False,
    }

    ids = []
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/plans", json=plan)
        ids.append(response.json()["_id"])

    to_block = [{"uid": id, "blocked": True} for id in ids]

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.patch(f"/plans", json=to_block)
    assert response.status_code == status.HTTP_200_OK

    for id in ids:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            plan = await app.mongodb[TRAININGS_COLLECTION_NAME].find_one({"_id": id})

            assert plan["blocked"] == True


@pytest.mark.anyio
async def test_block_user_wrong_body():
    plan = {
        "trainer": "Abdulazeez trainer",
        "title": "Pilates training plan",
        "description": "A pilates training plan",
        "difficulty": "beginner",
        "training_types": ["cardio"],
        "media": ["link-to-image", "link-to-video"],
        "goals": ["plank: one minute"],
        "duration": 30,
        "reviews": None,
        "blocked": False,
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/plans", json=plan)
    plan_id = response.json()["_id"]

    to_block = {}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.patch(f"/plans", json=to_block)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    async with AsyncClient(app=app, base_url="http://test") as ac:
        plan = await app.mongodb[TRAININGS_COLLECTION_NAME].find_one({"_id": plan_id})
    assert plan["blocked"] == False


@pytest.mark.anyio
async def test_block_plan_doesnt_exist():
    block = [{"uid": "abc", "blocked": True}]
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.patch(f"/plans", json=block)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_block_plan_doesnt_exist():
    block = [{"uid": "abc", "blocked": True}]
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.patch(f"/plans", json=block)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_users_adds_plan_as_favourite():
    plan = {
        "trainer": "Abdulazeez trainer",
        "title": "Pilates training plan",
        "description": "A pilates training plan",
        "difficulty": "beginner",
        "training_types": ["cardio"],
        "media": ["link-to-image", "link-to-video"],
        "goals": ["plank: one minute"],
        "duration": 30,
        "reviews": None,
        "blocked": False,
        "favourited_by": [],
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/plans", json=plan)
        id = response.json()["_id"]

    to_favourite = {"training_id": id}

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            f"/users/user_id/trainings/favourites", json=to_favourite
        )
    assert response.status_code == status.HTTP_200_OK

    async with AsyncClient(app=app, base_url="http://test") as ac:
        plan = await app.mongodb[TRAININGS_COLLECTION_NAME].find_one({"_id": id})
        assert plan["favourited_by"][0] == "user_id"


@pytest.mark.anyio
async def test_users_tries_to_add_nonexisting_plan_as_favourite():
    to_favourite = {"training_id": "abc"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            f"/users/user_id/trainings/favourites", json=to_favourite
        )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_user_deletes_favourite_from_plan():
    plan = {
        "trainer": "Abdulazeez trainer",
        "title": "Pilates training plan",
        "description": "A pilates training plan",
        "difficulty": "beginner",
        "training_types": ["cardio"],
        "media": ["link-to-image", "link-to-video"],
        "goals": ["plank: one minute"],
        "duration": 30,
        "reviews": None,
        "blocked": False,
        "favourited_by": ["user_id"],
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/plans", json=plan)
        id = response.json()["_id"]


    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(
            f"/users/user_id/trainings/favourites/{id}"
        )
        
    assert response.status_code == status.HTTP_204_NO_CONTENT

    async with AsyncClient(app=app, base_url="http://test") as ac:
        plan = await app.mongodb[TRAININGS_COLLECTION_NAME].find_one({"_id": id})
        assert plan["favourited_by"] == []

        
@pytest.mark.anyio
async def test_user_tries_to_delete_nonexisten_favourite_from_plan():
    to_favourite = {"training_id": "abc"}

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            f"/users/user_id/trainings/favourites", json=to_favourite
        )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_get_user_favourite_plans():
    trainer = "Abdulazeez trainer"
    plans = [
        {
            "trainer": trainer,
            "title": "Pilates training plan",
            "description": "A pilates training plan",
            "difficulty": "beginner",
            "training_types": ["cardio"],
            "media": ["link-to-image", "link-to-video"],
            "goals": ["plank: one minute"],
            "duration": 30,
            "reviews": None,
            "favourited_by": ["user_id"],
        },
        {
            "trainer": trainer,
            "title": "Crossfit training plan",
            "description": "A crossfit training plan",
            "difficulty": "intermediate",
            "training_types": ["cardio"],
            "media": ["link-to-image", "link-to-video"],
            "goals": ["plank: one minute"],
            "duration": 120,
            "reviews": None,
            "favourited_by": ["user_id"],
        },
        {
            "trainer": trainer,
            "title": "Pilates training plan",
            "description": "A pilates training plan",
            "difficulty": "beginner",
            "training_types": ["cardio"],
            "media": ["link-to-image", "link-to-video"],
            "goals": ["plank: one minute"],
            "duration": 30,
            "favourited_by": [],
        },
        {
            "trainer": trainer,
            "title": "Crossfit training plan",
            "description": "A crossfit training plan",
            "difficulty": "beginner",
            "training_types": ["cardio"],
            "media": ["link-to-image", "link-to-video"],
            "goals": ["plank: one minute"],
            "duration": 120,
            "favourited_by": ["user_id"],
        },
    ]

    for plan in plans:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/plans", json=plan)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/users/user_id/trainings/favourites")

    json_result = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(json_result) == 3
