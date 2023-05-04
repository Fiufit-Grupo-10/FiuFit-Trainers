def test_post_user(test_app):
    data = {"uid": "10", "email": "t@gmail.com", "username": "user"}
    response = test_app.post(url="/users", json=data)
    assert response.status_code == 200
    assert response.json() == {
        "uid": "10",
        "email": "t@gmail.com",
        "username": "user",
        "birthday": None,
        "level": None,
        "latitude": None,
        "longitude": None,
        "height": None,
        "weight": None,
        "gender": None,
        "target": None,
        "trainingtypes": [],
        "user_type": None,
    }


def test_post_user_uid_fail(test_app):
    data = {"uid": "10", "email": "t2@gmail.com", "username": "user2"}
    response = test_app.post(url="/users", json=data)
    assert response.status_code == 409
    assert response.json() == {"detail": "User with uid: 10 already exists"}


def test_post_user_username_fail(test_app):
    data = {"uid": "11", "email": "t2@gmail.com", "username": "user"}
    response = test_app.post(url="/users", json=data)
    assert response.status_code == 409
    assert response.json() == {"detail": "User with username: user already exists"}


def test_post_user_email_fail(test_app):
    data = {"uid": "11", "email": "t@gmail.com", "username": "user2"}
    response = test_app.post(url="/users", json=data)
    assert response.status_code == 409
    assert response.json() == {"detail": "User with email: t@gmail.com already exists"}


def test_put_user(test_app):
    data = {
        "email": "t@gmail.com",
        "username": "user",
        "height": "180",
        "weight": "75",
        "gender": "M",
        "target": "fat loss",
        "trainingtypes": ["Cardio", "Fuerza"],
        "birthday": "1999-12-21",
        "level": "pro",
        "latitude": "100",
        "longitude": "100",
        "user_type": "athlete",
    }
    response = test_app.put(url="/users/10", json=data)
    assert response.status_code == 200
    assert response.json() == {
        "uid": "10",
        "email": "t@gmail.com",
        "username": "user",
        "height": 180,
        "weight": 75,
        "gender": "M",
        "target": "fat loss",
        "trainingtypes": ["Cardio", "Fuerza"],
        "birthday": "1999-12-21",
        "level": "pro",
        "latitude": 100,
        "longitude": 100,
        "user_type": "athlete",
    }


def test_get_user(test_app):
    response = test_app.get(url="/users/10")
    assert response.status_code == 200
    assert response.json() == {
        "uid": "10",
        "email": "t@gmail.com",
        "username": "user",
        "height": 180,
        "weight": 75,
        "gender": "M",
        "target": "fat loss",
        "trainingtypes": ["Cardio", "Fuerza"],
        "birthday": "1999-12-21",
        "level": "pro",
        "latitude": 100,
        "longitude": 100,
        "user_type": "athlete",
    }


def test_get_users(test_app):
    response = test_app.get(url="/users")
    assert response.status_code == 200
    assert response.json() == [
        {
            "uid": "10",
            "email": "t@gmail.com",
            "username": "user",
            "height": 180,
            "weight": 75,
            "gender": "M",
            "target": "fat loss",
            "trainingtypes": ["Cardio", "Fuerza"],
            "birthday": "1999-12-21",
            "level": "pro",
            "latitude": 100,
            "longitude": 100,
            "user_type": "athlete",
        }
    ]


def test_get_user_fail(test_app):
    response = test_app.get(url="/users/25")
    assert response.status_code == 404
    assert response.json() == {"detail": "User 25 not found"}
