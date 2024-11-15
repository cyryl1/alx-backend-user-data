#!/usr/bin/env python3
"""User session authentication model"""

from models.base import Base


class UserSession(Base):
    """Class Representation of the UserSession"""
    def __init__(self, *args: list, **kwargs: dict):
        """
        Initialize class
        Args:
            *args: Arguments for Base class
            **kwargs: Keyword arguments for Base class
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
