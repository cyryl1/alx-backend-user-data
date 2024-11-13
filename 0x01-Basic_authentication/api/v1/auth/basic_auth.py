#!/usr/bin/env python3
"""Basic Authentication"""

from api.v1.auth.auth import Auth


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
