from app.api.trainers import routes
from app.config.database import TRAININGS_COLLECTION_NAME
from app.main import app
from httpx import AsyncClient
import pytest

def test_create_plan_without_errors(test_app):
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
        "media": ["link-to-image", "link-to-video"],
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
        "media": ["link-to-image", "link-to-video"],
        "goals": ["plank: one minute"],
        "duration": 90,
        "reviews": None,
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/plans", json=plan)
        
    id = response.json()["_id"]

    updated_plan =   {
                "title": "Updated training plan",
                "description": "Updated plan description",
                "difficulty": "advanced",
                "training_types": ["cardio","hiit"],
                "media": ["link-to-image", "link-to-video", "link-to-image2"],
                "goals": ["plank: two minute"],
                "duration": 30,
            }
    
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put(f"/plans/{id}", json=updated_plan)

    
    assert response.status_code == 200
    async with AsyncClient(app=app, base_url="http://test") as ac:
        current_plan = await app.mongodb[TRAININGS_COLLECTION_NAME].find_one({"_id": id})

    expected_plan = {
        "_id": id,
        "trainer": "c59710ef-f5d0-41ba-a787-ad8eb739ef4c",
        "title": "Updated training plan",
        "description": "Updated plan description",
        "difficulty": "advanced",
        "training_types": ["cardio","hiit"],
        "media": ["link-to-image", "link-to-video", "link-to-image2"],
        "goals": ["plank: two minute"],
        "duration": 30,
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
        "media": ["link-to-image", "link-to-video"],
        "goals": ["plank: one minute"],
        "duration": 90,
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/plans", json=plan)
        
    id = response.json()["_id"]

    updated_plan =  { }
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put(f"/plans/{id}", json=updated_plan)

    
    assert response.status_code == 200
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        current_plan = await app.mongodb[TRAININGS_COLLECTION_NAME].find_one({"_id": id})

    expected_plan = {
        "_id": id,
        "trainer": "c59710ef-f5d0-41ba-a787-ad8eb739ef4c",
        "title": "Sample training plan",
        "description": "Training plan description",
        "difficulty": "beginner",
        "training_types": ["cardio"],
        "media": ["link-to-image", "link-to-video"],
        "goals": ["plank: one minute"],
        "duration": 90,
    }

    assert current_plan == expected_plan


def test_update_unexisting_plan(test_app):
    
    updated_plan = {
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
    id = 'unexisting_id'

    response = test_app.put(f"/plans/{id}", json=updated_plan)
    assert response.status_code == 404



