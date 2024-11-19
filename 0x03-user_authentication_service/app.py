#!/usr/bin/env python3
"""Flask App"""

from flask import Flask, jsonify, request, abort, make_response
from flask import redirect
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=['GET'])
def main():
    """Testing"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def users():
    """
    POST /users endpoint to register a new user.

    Expects form data:
        - email: User's email
        - password: User's password

    Returns:
        JSON response indicating success or failure.
    """
    # data = request.get_json()
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": f"user created"}), 201
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """
    Endpoint for user login
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(400, description="Email and password required!")
    valid_login = AUTH.valid_login(email=email, password=password)
    if not valid_login:
        abort(401, description="Invalid login credentials")

    session_id = AUTH.create_session(email=email)
    if not session_id:
        abort(401, description="Invalid login credentials")

    response = make_response(
        jsonify({"email": email, "message": "logged in"})
    )
    response.set_cookie('session_id', session_id)

    return response


@app.route('/sessions', methods=['DELETE'])
def logout():
    """
    Logout endpoint. Gets the session_id from the cookie,
    Uses the session_id to get the user, if user exist destroy
    the session.
    """
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403, description="Session ID is required")
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403, description="Invalid session ID")

    AUTH.destroy_session(user.id)

    return redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
