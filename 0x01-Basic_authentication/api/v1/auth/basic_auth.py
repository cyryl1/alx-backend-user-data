#!/usr/bin/env python3
"""Basic Authentication"""

from api.v1.auth.auth import Auth
from models.user import User
import base64
from typing import TypeVar


class BasicAuth(Auth):
    """
    Class Representation of Basic Authentication
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extracts the credentials needed for authentication"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        base64_encoded_credentials = authorization_header[6:]
        return base64_encoded_credentials

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """Decodes base64 credentials"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_credentials = base64.b64decode(
                base64_authorization_header
                ).decode('utf-8')
            return decoded_credentials
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """
        Extracts the username and password from the decoded credentials
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        username, password = decoded_base64_authorization_header.split(":")
        return username, password

    def user_object_from_credentials(self,
                                     user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """Returns the instance based on his email and password"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        # user = User(email=user_email, password=user_pwd)
        # users = User.load_from_file()
        users = User.search({"email": user_email})
        if not users:
            return None

        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user
