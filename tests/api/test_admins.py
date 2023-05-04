def test_post_admin(test_app):
    data = {"uid": "20", "email": "admin@gmail.com", "username": "admin"}
    response = test_app.post(url="/admins", json=data)
    assert response.status_code == 200
    assert response.json() == {
        "uid": "20",
        "email": "admin@gmail.com",
        "username": "admin",
    }


def test_post_admin_uid_fail(test_app):
    data = {"uid": "20", "email": "admin2@gmail.com", "username": "admin2"}
    response = test_app.post(url="/admins", json=data)
    assert response.status_code == 409
    assert response.json() == {"detail": "Admin with uid: 20 already exists"}


def test_post_admin_username_fail(test_app):
    data = {"uid": "21", "email": "admin2@gmail.com", "username": "admin"}
    response = test_app.post(url="/admins", json=data)
    assert response.status_code == 409
    assert response.json() == {"detail": "Admin with username: admin already exists"}


def test_post_admin_email_fail(test_app):
    data = {"uid": "21", "email": "admin@gmail.com", "username": "admin2"}
    response = test_app.post(url="/admins", json=data)
    assert response.status_code == 409
    assert response.json() == {
        "detail": "Admin with email: admin@gmail.com already exists"
    }


def test_get_admin(test_app):
    response = test_app.get(url="/admins/20")
    assert response.status_code == 200
    assert response.json() == {
        "uid": "20",
        "email": "admin@gmail.com",
        "username": "admin",
    }


def test_get_admin_fail(test_app):
    response = test_app.get(url="/admins/25")
    assert response.status_code == 404
    assert response.json() == {"detail": "Admin 25 not found"}


def test_get_admins(test_app):
    response = test_app.get(url="/admins")
    assert response.status_code == 200
    assert response.json() == [
        {
            "uid": "20",
            "email": "admin@gmail.com",
            "username": "admin",
        }
    ]
