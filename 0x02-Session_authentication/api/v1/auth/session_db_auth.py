#!/usr/bin/env python3
"""Session DB Authentication"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime


class SessionDBAuth(SessionExpAuth):
    """Class Representation of Session DB Authentication"""
    def create_session(self, user_id=None):
        """
        Creates a stroe new instance of UserSession
        Parmaters:
            user_id (str): ID of the user
        Returns:
            session_id
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns the user ID based on a Session ID
        Parameters:
            session_id (str): ID of the session
        Returns:
            user_id
        """
        sessions = UserSession.search({'session_id': session_id})
        if not sessions or len(sessions) == 0:
            return None

        user_session = sessions[0]
        if self.session_duration <= 0:
            return user_session.user_id

        created_at = user_session.created_at
        if not created_at:
            return None

        expiration_time = created_at + self.session_duration
        if datetime.utcnow() > expiration_time:
            return None

        return user_session.user_id

    def destroy_session(self, request=None):
        """
        Destroys the session
        Parameters:
            request (Flask Request): Request object
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        sessions = UserSession.search({'session_id': session_id})
        if not sessions or len(sessions) == 0:
            return False

        session = session[0]
        session.remove()
        return True
