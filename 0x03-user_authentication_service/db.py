#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError, IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database

        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The added user object.
        """
        try:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
            return user
        except IntegrityError:
            self._session.rollback()
            raise ValueError(f"User {email} already exists.")

    def find_user_by(self, **kwargs):
        """
        Finds a user based on keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments to filter the query.

        Returns:
            User: The first matching user.

        Raises:
            NoResultFound: If no user matches the query.
            InvalidRequestError: If query arguments are invalid.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound("No user found with the provided query")
        except InvalidRequestError as e:
            return InvalidRequestError(f"Invalid query arguments: {e}")

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates a user with the attribute given
        filters using the user_id

        Args:
            user_id: (int)
            **kwargs: Arbitrary keyword argument to represent
                the attribute.
        Returns:
            None
        """
        try:
            user = self.find_user_by(id=user_id)

            for key, val in kwargs.items():
                if not hasattr(user, key):
                    raise ValueError(f"Invalid attribute: {key}")
                setattr(user, key, val)

            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise e

    def commit_changes(self) -> None:
        """Public method to commit changes to the database"""
        self._session.commit()

    def rollback_changes(self) -> None:
        """Public method to roll back changes to the database"""
        self._session.rollback()
