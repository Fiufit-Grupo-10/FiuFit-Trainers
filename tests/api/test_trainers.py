from app.api.trainers import routes


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
