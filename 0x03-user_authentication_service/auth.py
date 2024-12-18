#!/usr/bin/env python3
"""Authentication"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid
from typing import Optional


def _hash_password(password: str) -> bytes:
    """
    Hashes the password using bcrypt
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generate uuid
    Returns:
        a string representation of a new UUID
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists.")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Checks is credentials are valid
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
            return True
        else:
            return False

    def create_session(self, email: str) -> str:
        """
        Generates a uuid and stores as the session id
        Returns:
            session ID: str
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        user.session_id = session_id
        self._db.commit_changes()
        return session_id

    def get_user_from_session_id(self,
                                 session_id: Optional[str]) -> Optional[User]:
        """
        Finds a user using the session_id
        Args:
            session_id: str
        Returns:
            user object.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Removes the session id for a particular user
        Args:
            user_id: int
        Returns:
            None
        """
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
            self._db.commit_changes()
        except NoResultFound:
            pass
        except Exception as e:
            self._db.rollback_changes()
            raise e

    def get_reset_password_token(self, email: str) -> str:
        """
        Creates a reset token
        Args:
            email: str
        Returns:
            str
        """
        try:
            user = self._db.find_user_by(email=email)
        except ValueError:
            raise ValueError("Invalid email")
        reset_token = _generate_uuid()
        user.reset_token = reset_token
        return reset_token

    def update_password(self, rest_token: str, password: str) -> None:
        """
        This updates a password using the rest token
        Args:
            reset_token: str,
            password: str
        Returns:
            None
        """
        user = self._db.find_user_by(rest_token=rest_token)
        if not user:
            raise ValueError("Invalid reset token")
        hashed_password = _hash_password(password)
        user.hashed_password = hashed_password
        user.reset_token = None
        self._db.commit_changes()
