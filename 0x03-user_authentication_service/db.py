#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from user import User, Base


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
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
        Add a new user to the database.

        Args:
            email: The email of the user
            hashed_password: Hashed password of the user

        Returns:
            User: The newly created user object.
        """

        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by given filter arguments

        Args:
            **kwargs: Arbitrary keyword arguments to filter the user.

        Returns:
            User: The found user object.

        Raises:
            NoResultFound: When no user is found
            MultipleResultsFOund: When multiple users match the filter
            InvalidRequestError: When Invalid query arguments are passed
        """

        if not kwargs:
            raise InvalidRequestError

        user = self._session.query(User).filter_by(**kwargs).first()

        if user is None:
            raise NoResultFound
        else:
            return user
