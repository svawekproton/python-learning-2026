# Day 5: Flask-SQLAlchemy, Migrations & CLI Commands

Transitioning from in-memory data structures to a persistent relational database (SQLite) using SQLAlchemy 2.0. Implementing professional backend architecture with database migrations and custom CLI commands.

## Architecture

The project is split into multiple files to prevent Circular Import Errors (a common pitfall in Flask):
- `database.py`: Initializes the bare `db` object (Data Mapper pattern).
- `models.py`: Contains SQLAlchemy models inheriting from `Base` with a custom `to_dict()` serializer.
- `app.py`: The application factory that binds `db.init_app(app)` and registers routes.
- `seed.py`: Contains database seeding logic, isolated from the web server.

## Usage & Database Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run migrations to create the database (instance/project.db) and tables
flask db upgrade

# 3. Seed the database with initial data (Custom CLI command)
flask seed

# 4. Run the server
flask run --debug
```

## Features

- ✅ SQLAlchemy 2.0 Syntax: Using db.session.execute(db.select(User)) instead of legacy .query(), and db.session.get(User, id) for efficient Identity Map lookups.
- ✅ DTO Serialization: Added a to_dict() method to models for clean JSON serialization in the API layer.
- ✅ Database Migrations: Implemented Flask-Migrate (Alembic) to handle schema changes (like adding an email column) instead of basic db.create_all().
- ✅ Custom Flask CLI: Created a @app.cli.command("seed") to mimic rails db:seed functionality.
- ✅ Isolated Testing: Refactored pytest fixtures to use an in-memory SQLite database (sqlite:///:memory:) to ensure tests run fast and don't pollute the development database.

## Requirements

- Python 3.12+
- Flask
- pytest (for running tests)

## What I Learned (Ruby vs Python differences)

- Data Mapper vs Active Record: SQLAlchemy uses a Session (db.session.add(), db.session.commit()) to manage state, unlike Rails where objects save themselves (user.save).
- No Magic Serialization: Unlike render json: @user, SQLAlchemy objects must be explicitly serialized into dictionaries before passing to jsonify().
- CLI Ecosystem: Flask doesn't have Rake tasks out of the box. You build your own CLI tools using the integrated Click library (@app.cli.command()).
- Pathing: Always use absolute paths (os.path.abspath) for SQLite databases in Python, otherwise CLI commands and the web server might create/look for the .db file in different directories.
