import pytest
from app import app, users


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test_secret"

    with app.test_client() as client:
        yield client

        users.clear()
        users.extend(
            [
                {"id": 1, "name": "Alex", "role": "admin"},
                {"id": 2, "name": "Maria", "role": "user"},
            ]
        )


def test_get_all_users_html(client):
    response = client.get("/users")

    assert response.status_code == 200

    html = response.data.decode()

    assert "Alex" in html
    assert "Maria" in html
    assert "<form" in html
    assert 'name="name"' in html


def test_create_user_success(client):
    response = client.post(
        "/users", data={"name": "John", "role": "guest"}, follow_redirects=True
    )

    assert response.status_code == 200
    html = response.data.decode()

    assert "User created succesfully" in html
    assert "John" in html
    assert "guest" in html

def test_create_user_invalid_data(client):
    response = client.post("/users", data={"name": "John"})

    assert response.status_code == 400
    html = response.data.decode()
    assert "Invalid inputs" in html

def test_delete_user_success(client):
    response = client.post("/users/2/delete", follow_redirects=True)

    assert response.status_code == 200
    html = response.data.decode()

    assert "User deleted succesfully" in html
    assert "Maria" not in html
