# Day 3: Flask Hello World API + pytest

A minimalist REST API built with Flask, demonstrating fundamental Python web routing, JSON handling, and test-driven development using `pytest`.

## Usage

```bash
# Set up isolated environment (The Python Way)
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
flask --app app run --debug
```

## API Endpoints
The application manages an in-memory list of users and returns strictly application/json responses.

| Method | Endpoint      | Description                          | Success | Error Handling  |
| :----- | :------------ | :----------------------------------- | :-----: | :-------------- |
| GET    | `/users`      | Retrieve all users                   |   200   | -               |
| GET    | `/users/<id>` | Retrieve a specific user by ID       |   200   | 404 Not Found   |
| POST   | `/users`      | Create a new user (requires payload) |   201   | 400 Bad Request |
| DELETE | `/users/<id>` | Delete a user by ID                  |   200   | 404 Not Found   |

## Features

- ✅ RESTful Design: Strict adherence to HTTP methods (no Rails-style /users/new for API).
- ✅ Error Handling: Explicit return of JSON error messages with correct HTTP status codes instead of HTML default errors (abort(404)).
- ✅ Pythonic Data Filtering: Using generators and next() for $O(n)$ search, avoiding heavy list(filter(...)) operations.
- ✅ Test Coverage: Comprehensive testing suite covering both happy paths and edge cases (missing data, non-existent IDs).

## Requirements

- Python 3.12+
- Flask
- pytest (for running tests)

## What I Learned (Ruby vs Python differences)

- Dependency Management: Python requires Virtual Environments (venv). pip installs globally by default, unlike Bundler in Ruby. You must explicitly isolate your project.
- Microframework Philosophy: Flask is not Rails. There is no ORM out of the box, no rescue_from for global error handling. You are responsible for crafting every JSON response and status code manually.
- Testing: pytest is minimalist. No RSpec DSL (describe, context, it). It relies on standard assert statements and @pytest.fixture for dependency injection (replacing before/let).
- Data Querying: Replaced Ruby's users.select { |u| u[:id] == id } with Python's memory-efficient next((u for u in users if u["id"] == id), None).
