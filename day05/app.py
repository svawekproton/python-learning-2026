from flask import Flask, jsonify, request
from database import db
from models import User
from flask_migrate import Migrate
from seed import seed_users
import os

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, "instance", "project.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

db.init_app(app)

migrate = Migrate(app, db)


@app.route("/")
def welcome():
    return "Welcome to my API"


@app.route("/users")
def all_users():
    users = db.session.execute(db.select(User)).scalars().all()
    return jsonify([u.to_dict() for u in users])


@app.route("/users/<int:user_id>")
def show_user(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    else:
        return jsonify(user.to_dict())


@app.post("/users")
def new_user():
    name = request.json.get("name")
    role = request.json.get("role")
    email = request.json.get("email")
    if name is None or role is None or email is None:
        return jsonify({"error": "Name, role and email are required"}), 400
    else:
        user = User(name=name, role=role, email=email)
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict())


@app.delete("/users/<int:user_id>")
def delete_user(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    else:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"result": "User deleted"})


@app.cli.command("seed")
def seed_command():
    """Seed the database with initial data."""
    with app.app_context():
        seed_users()
