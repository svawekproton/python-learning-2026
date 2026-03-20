from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, jsonify, request, g
from models import User, Post
from database import db
from flask_migrate import Migrate
from decorators import login_required
from sqlalchemy.orm import joinedload
import os

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, "instance", "project.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

db.init_app(app)
migrate = Migrate(app, db)


@app.post("/register")
def register():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "Missing data"}), 400

    existing_user = db.session.execute(
        db.select(User).where(User.email == email)
    ).scalar()
    if existing_user:
        return jsonify({"error": "User with this email already exists"}), 400

    hashed_password = generate_password_hash(password)

    new_user = User(name=name, email=email, password_hash=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201


@app.post("/login")
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = db.session.execute(db.select(User).where(User.email == email)).scalar()
    if user and check_password_hash(user.password_hash, password):
        return jsonify({"token": f"simple-token-{user.id}"})
    else:
        return jsonify({"error": "Invalid email or password"}), 401


@app.get("/posts")
def get_posts():
    posts = (
        db.session.execute(db.select(Post).options(joinedload(Post.author)))
        .scalars()
        .all()
    )
    return jsonify([post.to_dict() for post in posts])


@app.post("/posts")
@login_required
def create_post():
    data = request.json
    title = data.get("title")
    description = data.get("description")
    user_id = g.current_user_id

    post = Post(title=title, description=description, author_id=user_id)
    db.session.add(post)
    db.session.commit()

    return jsonify({"message": "Post created", "id": post.id}), 201


@app.get("/posts/<int:post_id>")
def get_post(post_id: int):
    post = db.session.execute(
        db.select(Post).where(Post.id == post_id).options(joinedload(Post.author))
    ).scalar_one_or_none()
    if post is None:
        return jsonify({"error": "Post not found"}), 404
    return jsonify(post.to_dict())


@app.post("/posts/<int:post_id>")
@login_required
def update_post(post_id: int):
    post = db.session.execute(
        db.select(Post).where(Post.id == post_id)
    ).scalar_one_or_none()
    if post is None:
        return jsonify({"error": "Post not found"}), 404
    if post.author_id != g.current_user_id:
        return jsonify({"error": "You are not authorised to update this post"}), 403
    data = request.json
    if data.get("title"):
        post.title = data.get("title")
    if data.get("description"):
        post.description = data.get("description")
    db.session.commit()
    return jsonify({"message": "Post updated", "id": post.id})


@app.delete("/posts/<int:post_id>")
@login_required
def delete_post(post_id: int):
    post = db.session.execute(
        db.select(Post).where(Post.id == post_id)
    ).scalar_one_or_none()
    if post is None:
        return jsonify({"error": "Post not found"}), 404
    if post.author_id != g.current_user_id:
        return jsonify({"error": "You are not authorised to delete this post"}), 403
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted", "id": post.id})


@app.get("/users/<int:user_id>/posts")
def get_user_posts(user_id: int):
    posts = (
        db.session.execute(db.select(Post).where(Post.author_id == user_id).options(joinedload(Post.author)))
        .scalars()
        .all()
    )
    return jsonify([post.to_dict() for post in posts])
