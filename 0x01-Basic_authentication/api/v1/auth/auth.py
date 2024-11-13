from flask import request
from typing import List, TypeVar
"""Authentication"""


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if the request path is authenticated"""
        return False
    

    def authorization_header(self, request=None) -> str:
        """Returns the authorization header from the request"""
        return None
    

    def current_user(self, request=None) -> TypeVar('User'):
        return None
