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
        return jsonify({"email": email, "message": "user created"}), 201
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
        abort(401, description="Email and password required!")
    if not AUTH.valid_login(email=email, password=password):
        abort(401, description="Invalid login credentials")

    session_id = AUTH.create_session(email=email)
    if not session_id:
        abort(401, description="could not create session")

    response = make_response(
        jsonify({"email": email, "message": "logged in"})
    )
    response.set_cookie('session_id', session_id)

    return response, 200


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


@app.route('/profile', methods=['GET'])
def profile():
    """
    Returns the user profile
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403, description="Invalid session_id")

    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """
    Gets the reset_token
    """
    email = request.form.get('email')
    reset_token = AUTH.get_reset_password_token(email=email)
    if not reset_token:
        abort(403)
    return jsonify({
        "email": email,
        "reset_token": reset_token
    }), 200


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """
    This updates the password
    """
    try:
        email = request.form.get('email')
        reset_token = request.form.get('reset_token')
        new_password = request.form.get('new_password')
        update = AUTH.update_password(
            rest_token=reset_token,
            password=new_password
        )
        if update:
            return jsonify({
                "email": email,
                "message": "Password updated"
            }), 200
    except ValueError:
        return jsonify({"message": "Invalid reset_token"}), 403
        # abort(403, description="Invalid reset_token")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
