from app.api.trainers import routes
from app.config.database import TRAININGS_COLLECTION_NAME


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


async def test_update_existing_plan(test_app):
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
    
    

    response = test_app.put(f"/plans/{id}", json=updated_plan)

    
    assert response.status_code == 200

    current_plan = await test_app.app.mongodb[TRAININGS_COLLECTION_NAME].find_one({"_id": id})

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
        "reviews": None,
    }

    assert current_plan == expected_plan



# def test_modify_plan(test_app):
#     plan = {
#         "trainer": "c59710ef-f5d0-41ba-a787-ad8eb739ef4c",
#         "title": "Sample training plan",
#         "description": "Training plan description",
#         "difficulty": "beginner",
#         "training_types": ["cardio"],
#         "media": ["link-to-image", "link-to-video"],
#         "goals": ["plank: one minute"],
#         "duration": 90,
#         "reviews": None,
#     }

#     response = test_app.post("/plans", json=plan)
#     assert response.status_code == 201

#     body = response.json()

#     new_plan = {
#         "title": "New Sample training plan",
#         "description": "New training plan description",
#         "difficulty": "hard",
#         "training_types": ["cardio", "hiit"],
#         "media": ["link-to-image", "link-to-video"],
#         "goals": ["plank: one minute"],
#         "duration": 30,
#     }

#     id = body["_id"]
#     response = test_app.put(f"/plans/{id}")
#     routes
