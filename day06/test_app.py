import pytest
from app import app, db
from models import User, Post
from werkzeug.security import generate_password_hash

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

 
@pytest.fixture
def test_user(client):
    user = User(
        name="Test User",
        email="test@example.com",
        password_hash=generate_password_hash("password")
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def test_post(client, test_user):
    post = Post(
        title="Test Post", 
        description="Test Description", 
        author_id=test_user.id
    )
    db.session.add(post)
    db.session.commit()
    return post


@pytest.fixture
def auth_headers(test_user):
    return {"Authorization": f"Bearer simple-token-{test_user.id}"}

def test_register(client):
    response = client.post("/register", json={
        "name": "New User",
        "email": "new@example.com",
        "password": "newpassword"
    })
    assert response.status_code == 201
    assert "id" in response.json
    assert response.json["email"] == "new@example.com"

def test_register_missing_data(client):
    response = client.post("/register", json={"name": "New User"})
    assert response.status_code == 400
    assert "error" in response.json

def test_register_existing_user(client, test_user):
    response = client.post("/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "password"
    })
    assert response.status_code == 400
    assert "already exists" in response.json["error"]

def test_login_success(client, test_user):
    response = client.post("/login", json={
        "email": "test@example.com",
        "password": "password"
    })
    assert response.status_code == 200
    assert "token" in response.json

def test_login_invalid(client, test_user):
    response = client.post("/login", json={
        "email": "test@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_get_posts(client, test_post):
    response = client.get("/posts")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["title"] == "Test Post"
    assert response.json[0]["author"]["name"] == "Test User"

def test_create_post(client, auth_headers):
    response = client.post("/posts", headers=auth_headers, json={
        "title": "New Post",
        "description": "New Description"
    })
    assert response.status_code == 201
    assert response.json["message"] == "Post created"

def test_create_post_unauthorized(client):
    response = client.post("/posts", json={
        "title": "New Post",
        "description": "New Description"
    })
    assert response.status_code == 401

def test_get_post(client, test_post):
    response = client.get(f"/posts/{test_post.id}")
    assert response.status_code == 200
    assert response.json["title"] == "Test Post"

def test_get_post_not_found(client):
    response = client.get("/posts/999")
    assert response.status_code == 404

def test_update_post(client, test_post, auth_headers):
    response = client.post(f"/posts/{test_post.id}", headers=auth_headers, json={
        "title": "Updated Title"
    })
    assert response.status_code == 200
    assert response.json["message"] == "Post updated"
    
    # Verify update
    updated_post = client.get(f"/posts/{test_post.id}")
    assert updated_post.json["title"] == "Updated Title"

def test_update_post_unauthorized_user(client, test_post):
    other_user = User(
        name="Other User", 
        email="other@example.com", 
        password_hash=generate_password_hash("password")
    )
    db.session.add(other_user)
    db.session.commit()
    
    other_headers = {"Authorization": f"Bearer simple-token-{other_user.id}"}
    response = client.post(f"/posts/{test_post.id}", headers=other_headers, json={
        "title": "Malicious Update"
    })
    assert response.status_code == 403

def test_delete_post(client, test_post, auth_headers):
    response = client.delete(f"/posts/{test_post.id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json["message"] == "Post deleted"
    
    verify_deleted = client.get(f"/posts/{test_post.id}")
    assert verify_deleted.status_code == 404

def test_delete_post_unauthorized_user(client, test_post):
    other_user = User(
        name="Other User", 
        email="other@example.com", 
        password_hash=generate_password_hash("password")
    )
    db.session.add(other_user)
    db.session.commit()
    
    other_headers = {"Authorization": f"Bearer simple-token-{other_user.id}"}
    response = client.delete(f"/posts/{test_post.id}", headers=other_headers)
    assert response.status_code == 403

def test_get_user_posts(client, test_user, test_post):
    response = client.get(f"/users/{test_user.id}/posts")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["title"] == "Test Post"
