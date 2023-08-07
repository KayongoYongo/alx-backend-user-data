#!/usr/bin/env python3
"""Auth class"""
from flask import request


class Auth:
    """This class manages API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Require auth

        Parameters:
            path: More to come
            exluded_paths: more to come

        Returns:
            False
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Deals with authorization header

        Parameters:
             request (flask.Request, optional): The Flask request object

        Returns:
            None
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Deals with current user

        Parameter:
            request :Flask request object

        Returns:
            None
        """
        return None
