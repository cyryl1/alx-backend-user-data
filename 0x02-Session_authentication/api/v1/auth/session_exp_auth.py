#!/usr/bin/env python3
"""Expiration for a Session ID"""
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Class Representation of the Session Expiration"""
    def __init__(self):
        """Initialzing the class"""
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Creates a Session ID with expiration details
        Parameter:
            user_id: User ID (string)
        Returns:
            session-id
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns the user ID based on a Session ID
        Parameter:
            session_id: Session ID (string)
        Returns:
            user_id
        """
        if session_id is None:
            return None
        session = self.user_id_by_session_id.get(session_id)
        if session is None:
            return None
        if self.session_duration <= 0:
            return session.get('user_id')
        if session['created_at'] is None:
            return None
        expiration_time = (session['created_at'] +
                           timedelta(self.session_duration))
        if datetime.now() > expiration_time:
            return None
        return session['user_id']
