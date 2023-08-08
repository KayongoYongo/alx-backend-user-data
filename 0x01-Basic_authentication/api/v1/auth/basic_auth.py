#!/usr/bin/env python3
"""A clas that impliments the Basic Auth
"""
import base64
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    This class impliments the basic implimentation

    Parameters:
        It imports from Auth

    Return:
        None
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        This method extracts the base 64 header

        parameter:
            authorization header - the header to be queried

        return:
            None or value after basic
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        required_value = authorization_header[6:]
        return required_value

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        This method decodes the base_64 header

        Parameter:
            base64_authorization_header: The header to be decoded
            from base_64

        Return:
            The decoded value
        """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_string = decoded_bytes.decode('utf-8')
            return decoded_string
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        This method is responsible for returning the decoded email
        and password.

        Parameters:
            decoded_base64_authorization_header - The header to be decoded

        Return:
            user email and password separated by a ":"
        """
        if decoded_base64_authorization_header is None:
            return (None, None)

        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)

        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        user_email, user_password = decoded_base64_authorization_header.\
            split(':', 1)
        return user_email, user_password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        This method returns the user insance

        Parameters:
            user_email: The email of the user
            user_pwd: The password of the user

        Return:
            An instance of the user
        """
        if user_email is None or isinstance(user_email, str):
            return None

        if user_pwd is None or isinstance(user_pwd, str):
            return None

        try:
            # Search for the User instance based on email
            users = User.search({'email': user_email})

            if not users or users == []:
                return None

            user = users[0]

            if user.is_valid_password(user_pwd):
                return user
            return None
        except Exception:
            return None
