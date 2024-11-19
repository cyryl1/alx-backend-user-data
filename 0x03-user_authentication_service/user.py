#!/usr/bin/env python3
"""A model to store the User details using mapping declaration"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
import logging

# Suppress SQLAlchemy logs
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

Base = declarative_base()


class User(Base):
    """Class User mapped"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), unique=True, nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
