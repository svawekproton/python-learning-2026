from flask import Flask, jsonify, request, abort

app = Flask(__name__)

users = [
    {"id": 1, "name": "Alex", "role": "admin"},
    {"id": 2, "name": "Maria", "role": "user"},
]


def find_user(user_id: int):
    return next((user for user in users if user["id"] == user_id), None)


@app.route("/")
def welcome():
    return "Welcome to my API"


@app.route("/users")
def all_users():
    return jsonify(users)


@app.route("/users/<int:user_id>")
def show_user(user_id):
    user = find_user(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    else:
        return jsonify(user)


@app.post("/users")
def new_user():
    name = request.json.get("name")
    role = request.json.get("role")
    if name is None or role is None:
        return jsonify({"error": "Name and role are required"}), 400
    else:
        id = max((user["id"] for user in users), default=0) + 1
        user = {"id": id, "name": name, "role": role}
        users.append(user)
        return jsonify(user)


@app.delete("/users/<int:user_id>")
def delete_user(user_id):
    user = find_user(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    else:
        users.remove(user)
        return jsonify(user)
