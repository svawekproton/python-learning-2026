# Day 4: Flask Forms, Jinja2 & Server-Side Rendering (SSR)

Transitioning from a pure JSON REST API to a classical Server-Side Rendered application using Flask's built-in templating engine, Jinja2.

## Usage

```bash
# Set up isolated environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
flask --app app run --debug
```

## API Endpoints
The application manages an in-memory list of users and returns strictly application/json responses.

| Method | Endpoint                  | Action                               |  Response Type |
| :----- | :------------------------ | :----------------------------------- | :------------- |
| GET    | `/users`                  | Renders the user list & create form  |   HTML (200)   |
| POST   | `/users`                  | Creates user from form data          | Redirect (302) |
| POST   | `/users/<user_id>/delete` | Deletes user by ID                   | Redirect (302) |

## Features

- ✅ Server-Side Rendering: Using render_template to generate HTML dynamically via Jinja2.
- ✅ Template Inheritance: Implementing a base.html layout that child templates (index.html) extend via {% block content %}.
- ✅ RG Pattern (Post/Redirect/Get): Preventing duplicate form submissions by returning a 302 Redirect (redirect(url_for(...))) after successful POST requests, instead of rendering HTML directly.
- ✅ State Management (Flash Messages): Using Flask's flash() mechanism via session cookies to pass transient success/error messages across requests.
- ✅ HTML Form Workarounds: Using POST methods to simulate DELETE actions, as native HTML forms only support GET and POST.

## Requirements

- Python 3.12+
- Flask
- pytest (for running tests)

## What I Learned (Ruby vs Python differences)

- Templating: Jinja2 ({% ... %}) is the Python ecosystem's equivalent to Ruby's ERB (<% ... %>).
- Data Extraction: In APIs, you use request.json. For HTML forms (application/x-www-form-urlencoded), you must use request.form.get("key").
- Delete Method Limitation: Rails abstracts away the lack of HTML form DELETE support using _method and JavaScript out of the box. In Flask, you must explicitly handle it (e.g., via a specific POST route like /delete).
- Routing Organization: Splitting GET and POST handlers into separate functions (e.g., @app.route vs @app.post) keeps controllers clean, avoiding messy if request.method == 'POST' logic.
