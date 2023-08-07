#!/usr/bin/env python3
"""Auth class"""
from flask import request
from typing import List, TypeVar


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
        if path is None:
            return True

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Ensure all excluded paths end with a slash for proper matching
        excluded_paths = [p if p.endswith('/') else
                          p + '/' for p in excluded_paths]

        # Add a slash to the input path if it doesn't have one
        path = path if path.endswith('/') else path + '/'

        # Check if the path is in the list of excluded paths
        return path not in excluded_paths

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
