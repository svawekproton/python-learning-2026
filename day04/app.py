from flask import Flask, render_template, redirect, url_for, request, flash

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

users = [
    {"id": 1, "name": "Alex", "role": "admin"},
    {"id": 2, "name": "Maria", "role": "user"},
]


def find_user(user_id: int):
    return next((user for user in users if user["id"] == user_id), None)


@app.route("/users")
def all_users():
    return render_template("index.html", users=users)


@app.post("/users")
def create_user():
    name = request.form.get("name")
    role = request.form.get("role")
    if not name or not role:
        return render_template("index.html", users=users, error="Invalid inputs"), 400

    id = max((user["id"] for user in users), default=0) + 1
    users.append({"id": id, "name": name, "role": role})

    flash("User created succesfully")
    return redirect(url_for("all_users"))


@app.post("/users/<int:user_id>/delete")
def delete_user(user_id):
    user = find_user(user_id)
    if user is None:
        flash("User not found")
    else:
        users.remove(user)
        flash("User deleted succesfully")

    return redirect(url_for("all_users"))
