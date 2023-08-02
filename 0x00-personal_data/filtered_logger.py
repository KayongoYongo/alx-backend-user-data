#!/usr/bin/env python3
"""Returns an obusfcated log message"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """This function obusfcates a string

    Args:
        fields: a list of strings representing all fields to obfuscate
        redaction: a string representing by what the field will be obfuscated
        message: a string representing the log line
        separator: a string representing by which character is
        separating all fields in the log line (message)

    Returns:
        A log message obfuscated
    """

    for field in fields:
        pattern = r'{0}={1}(?={2}|$)'.format(
            field, r'[^{0}]*?'.format(separator), re.escape(separator))
        message = re.sub(pattern, f'{field}={redaction}', message)
    return message
