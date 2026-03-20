from functools import wraps
from flask import jsonify, g, request


def login_required(f):
    @wraps(f)
    def decorated_login_required(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer simple-token-"):
            return jsonify({"error": "Unauthorized"}), 401
        try:
            token = auth_header.split(" ")[1]
            user_id = int(token.split("-")[2])
            g.current_user_id = user_id
        except (IndexError, ValueError):
            return jsonify({"error": "Invalid token format"}), 401
        return f(*args, **kwargs)

    return decorated_login_required
