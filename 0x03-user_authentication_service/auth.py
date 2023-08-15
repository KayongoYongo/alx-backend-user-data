#!/usr/bin/env python3
"""A function that encrypts a password
"""
import bcrypt


def _hash_password(password):
    """
    A method for hashing out a password

    Args:
        Password: The string to be hashed out

    Return:
        The password in byte format
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
