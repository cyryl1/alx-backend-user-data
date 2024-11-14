#!/usr/bin/env python3
"""Authentication"""

from flask import request
from typing import List, TypeVar
import fnmatch


class Auth:
    """
    Authentication class template
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if the request path is authenticated"""
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        for excluded_path in excluded_paths:
            if not excluded_path.endswith('/'):
                excluded_paths.append(excluded_path + '/')

        norm_path = path if path.endswith('/') else path + '/'
        for excluded_path in excluded_paths:
            if norm_path.startswith(excluded_path):
                return False

        for excluded_path in excluded_paths:
            if fnmatch.fnmatch(path, excluded_path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Returns the authorization header from the request"""
        if request is None:
            return None
        response = request.headers.get('Authorization')
        if response is None:
            return None
        else:
            return response

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns the current authenticated user based
        on the authorization header
        """
        return None
    
    def session_cookie(self, request=None):
        """Session cookie"""
        if request is None:
            return None
        
