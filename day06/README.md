# Day 6: Blog API with Authentication

A RESTful Blog API built with Flask featuring token-based authentication, ownership protection, and relationship-aware serialization.

## Usage

```bash
pip install -r requirements.txt
flask db upgrade
flask run --debug
```


## Architecture

- `app.py` — Routes and business logic
- `models.py` — SQLAlchemy models (`User`, `Post`) with `to_dict()` serialization
- `decorators.py` — `@login_required` decorator for protecting endpoints
- `database.py` — Isolated `db` object to prevent circular imports


## API Endpoints

| Method | Endpoint | Auth | Description |
| :-- | :-- | :--: | :-- |
| POST | `/register` | ✗ | Register a new user |
| POST | `/login` | ✗ | Login and receive a token |
| GET | `/posts` | ✗ | Get all posts (with authors) |
| POST | `/posts` | ✓ | Create a post |
| GET | `/posts/<id>` | ✗ | Get a single post |
| POST | `/posts/<id>` | ✓ | Update own post |
| DELETE | `/posts/<id>` | ✓ | Delete own post |
| GET | `/users/<id>/posts` | ✗ | Get all posts by a specific user |

## Authentication Flow

1. Register via `POST /register`.
2. Login via `POST /login` → receive a token (`simple-token-{user_id}`).
3. Pass the token in every protected request as a header:

```
Authorization: Bearer simple-token-1
```

4. The `@login_required` decorator validates the token and injects `g.current_user_id` into the request context.

## Security

- Passwords are never stored in plain text — hashed via `werkzeug.security.generate_password_hash`.
- Ownership is enforced server-side: users receive `403 Forbidden` if they attempt to modify another user's post.


## Testing

```bash
pytest
```

Tests use an in-memory SQLite database (`sqlite:///:memory:`) via a shared `client` fixture that manages `app_context` lifecycle. All dependent fixtures (`test_user`, `test_post`) inherit the active context automatically.

Covered scenarios:

- Registration (success, missing data, duplicate email)
- Login (success, wrong password)
- Post CRUD (with and without token)
- Ownership protection (`403` on unauthorized update/delete)


## What I Learned

- **Custom Decorators:** Built `@login_required` from scratch using `functools.wraps` — Python's equivalent of Rails' `before_action`.
- **Flask `g` object:** Used `g.current_user_id` to safely pass data between a decorator and a route handler within a single request lifecycle.
- **`DetachedInstanceError`:** SQLAlchemy objects become detached when their session closes. Fixture dependencies must share a single `app_context` — not open separate ones.
- **`joinedload` in practice:** Applied eager loading on `Post.author` across all endpoints to eliminate N+1 queries.