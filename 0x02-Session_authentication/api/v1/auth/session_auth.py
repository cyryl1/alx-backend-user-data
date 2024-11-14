#!/usr/bin/env python3
"""Session Authentication"""

from api.v1.auth.auth import Auth
import uuid
from api.v1.views.users import User
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login():
    """Handles login for session authentication"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email is missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})
    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)

    response = make_response(user.to_json())
    session_name = getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)

    return response


class SessionAuth(Auth):
    """
    Class Representation of Session Authentication
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create a session id
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(
            self,
            session_id: str = None
            ) -> str:
        """Returns ID based on a Session ID"""

        if session_id is None or isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Returns a user instance based on a cookie value"""
        session_id = self.session_cookie(request)

        if session_id is None:
            return None
        user_id = self.user_id_by_session_id.get(session_id)

        if user_id:
            return User.get(user_id)
        return None
