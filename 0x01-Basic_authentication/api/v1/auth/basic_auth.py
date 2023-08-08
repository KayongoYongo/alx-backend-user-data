#!/usr/bin/env python3
"""A clas that impliments the Basic Auth
"""
from api.v1.auth.auth import Auth


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
