import pytest
from app import app
from database import db
from models import User


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()

        user1 = User(name="Alex", role="admin", email="test1@test.com")
        user2 = User(name="Maria", role="user", email="test2@test.com")
        db.session.add_all([user1, user2])
        db.session.commit()

    with app.test_client() as client:
        yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()


def test_get_all_users(client):
    response = client.get("/users")

    assert response.status_code == 200

    data = response.get_json()
    assert len(data) == 2
    assert data[0]["name"] == "Alex"


def test_create_user_success(client):
    response = client.post(
        "/users", json={"name": "Anton", "role": "user", "email": "test3@test.com"}
    )

    assert response.status_code == 200

    data = response.get_json()
    assert data["name"] == "Anton"
    assert data["role"] == "user"

    with app.app_context():
        assert db.session.query(User).count() == 3


def test_create_user_missing_data(client):
    response = client.post("/users", json={"name": "Anton"})

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
    assert data["email"] == "test1@test.com"


def test_show_user_not_found(client):
    response = client.get("/users/999")

    assert response.status_code == 404
    assert "error" in response.get_json()
