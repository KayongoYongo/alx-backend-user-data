#!/usr/bin/env python3
"""This function hashes out a password"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes the given password with salting using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted, hashed password as a byte string.
    """
    # Convert the password to bytes as bcrypt expects bytes input
    password_bytes = password.encode('utf-8')

    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password
