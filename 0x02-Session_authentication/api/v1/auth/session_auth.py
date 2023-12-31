#!/usr/bin/env python3
"""A class that impliments session auth
"""
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """
    This class deals with session Authentication
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        This function creates a session.

        Parameters:
            user_id: The parameter used to create a session

        Return:
            None or a string
        """
        if user_id is None:
            return None

        if not isinstance(user_id, str):
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        This function returns a user ID based on session ID

        Parameters:
            session_id: The ID of the session

        Returns:
            A user_id based on session id
        """
        if session_id is None:
            return None

        if not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)
