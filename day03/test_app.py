import pytest
from app import app, users

@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

        users.clear()
        users.extend([
            {"id": 1, "name": "Alex", "role": "admin"},
            {"id": 2, "name": "Maria", "role": "user"}
        ])

def test_get_all_users(client):
    response = client.get("/users")

    assert response.status_code == 200

    data = response.get_json()
    assert len(data) == 2
    assert data[0]["name"] == "Alex"

def test_create_user_success(client):
    response = client.post("/users", json={"name": "Anton", "role": "user" })

    assert response.status_code == 200

    data = response.get_json()
    assert data["name"] == "Anton"
    assert data["role"] == "user"

def test_create_user_missing_data(client):
    response = client.post("/users", json={"name": "Anton" })

    assert response.status_code == 400
    assert "error" in response.get_json()

def test_delete_user_not_found(client):
    response = client.delete("/users/999")

    assert response.status_code == 404
    assert "error" in response.get_json()

def test_show_user_success(client):
    response = client.get("/users/1")

    assert response.status_code == 200

    data = response.get_json()
    assert data["name"] == "Alex"
    assert data["role"] == "admin"

def test_show_user_not_found(client):
    response = client.get("/users/999")

    assert response.status_code == 404
    assert "error" in response.get_json()
