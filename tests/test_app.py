import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


@pytest.fixture
def user_data():
    return {"first_name": "Luke", "last_name": "Barrett", "date_of_birth": "1998-06-12"}


def test_create_user(user_data):
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == user_data["first_name"]
    assert data["last_name"] == user_data["last_name"]
    assert data["date_of_birth"] == user_data["date_of_birth"]


@pytest.mark.parametrize(
    "filter_param, filter_value, expected_field",
    [
        ("first_name", "Luke", "first_name"),
        ("last_name", "Barrett", "last_name"),
        ("date_of_birth", "1998-06-12", "date_of_birth"),
    ],
)
def test_get_user(user_data, filter_param, filter_value, expected_field):
    client.post("/users/", json=user_data)

    response = client.get(f"/users/?{filter_param}={filter_value}")
    assert response.status_code == 200
    data = response.json()

    assert len(data) > 0
    assert data[0][expected_field] == filter_value


def test_get_user_not_found(user_data):
    client.post("/users/", json=user_data)

    response = client.get("/users/", params={"first_name": "Tommy"})
    assert response.status_code == 404


def test_user_not_found():
    response = client.get("/users/?first_name=TEST")
    assert response.status_code == 404
    assert response.json() == {
        "message": "No users found matching the provided filters.",
        "status": "error",
        "path": "/users/",
    }


def test_invalid_date_format():
    response = client.get("/users/?date_of_birth=12-06-1997")
    assert response.status_code == 400
    assert response.json() == {
        "message": "Invalid date format. Use 'YYYY-MM-DD'.",
        "status": "error",
        "path": "/users/",
    }
