def test_get_trainingtypes(test_app):
    response = test_app.get(url="/trainingtypes")
    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "Cardio",
            "descr": "Entrenamientos relacionados a la resistencia aerobica",
        },
        {"name": "Fuerza", "descr": "Entrenamientos relacionados a ganar fuerza"},
    ]
