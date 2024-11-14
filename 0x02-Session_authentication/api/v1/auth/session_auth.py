#!/usr/bin/env python3
"""Session Authentication"""

from api.v1.auth.auth import Auth
import uuid
from api.v1.views.users import User


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
