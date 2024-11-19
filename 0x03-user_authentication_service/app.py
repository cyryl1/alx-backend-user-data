#!/usr/bin/env python3
"""Flask App"""

from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
