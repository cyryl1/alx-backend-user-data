#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv  # Import os for environment variable access
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.auth import Auth
from api.v1.auth.session_exp_auth import SessionExpAuth


app = Flask(__name__)
app.register_blueprint(app_views)
# Allow cross-origin requests for all routes under /api/v1/*
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
auth_type = os.getenv('AUTH_TYPE')
if auth_type == "basic_auth":
    auth = BasicAuth()
elif auth_type == "session_auth":
    auth = SessionAuth()
elif auth_type == "session_exp_auth":
    auth = SessionExpAuth()
else:
    auth = Auth()


@app.before_request
def before_request():
    """
    Runs before each request to handle authentication checks.

    Checks if the request path requires authentication. If so, validates
    the authorization header or session cookie. Sets the current_user
    in the request object if authentication is successful.

    Raises:
        401: If no valid authentication is provided.
        403: If the user cannot be authenticated.
    """
    if auth is None:
        return
    path = request.path
    excluded_paths = ['/api/v1/status/',
                      '/api/v1/unauthorized/',
                      '/api/v1/forbidden/',
                      '/api/v1/auth_session/login/']
    if not auth.require_auth(path, excluded_paths):
        return
    if (auth.authorization_header(request) is None
            and auth.session_cookie(request) is None):
        abort(401)
    user = auth.current_user(request)
    if user is None:
        abort(403)
    request.current_user = user


@app.errorhandler(404)
def not_found(error) -> str:
    """
    Handles the Error Not found.
    Parameter:
        - Error
    Return:
        - 404 if Not Found
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    Unauthorized handler
    Parameter:
        - Error
    Return:
        - 401 if Unauthorized
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    Forbidden handler
    Parameter:
        - Error
    Return:
        - 403 if Forbidden
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    # Start the Flask application with the specified host and port
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
