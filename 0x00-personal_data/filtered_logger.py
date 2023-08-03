#!/usr/bin/env python3
"""Returns an obusfcated log message"""
import re
from typing import List
import logging
import os
from mysql.connector.connection import MySQLConnection


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        This function initializes a RedactingFormater instance.

        args:
            fields: a list of strings reperesenting all fields to obfuscate.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        This function formats a log message

        args:
            record: The file to be formatted
        """
        log_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, log_message,
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    This function creates a logger object called user-data.

    Return:
        A Logger object with INFO log level and RedactingFormatter
        formatter for filtering PII fields
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    pii_fields = ('name', 'email', 'phone', 'ssn', 'password')
    formatter = RedactingFormatter(pii_fields)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    This function obusfcates a string

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


def get_db() -> MySQLConnection:
    """
    This function returns a connector to the MySQL database.

    Returns:
    mysql.connector.connection.MySQLConnection: Database connection object
    """
    # Get credentials from environment variables with default values
    db_username = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    db_password = os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.environ.get('PERSONAL_DATA_DB_NAME')

    # Create a connection to the MySQL database
    connection = mysql.connector.connect(
        user=db_username,
        password=db_password,
        host=db_host,
        database=db_name
    )

    return connection


def main() -> None:
    """
    The main function to retrieve and display filtered data
    from the users table.
    """
    # Create the logger
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Set up the formatter
    PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Get the database connection
    db = get_db()
    cursor = db.cursor()

    # Retrieve all rows from the users table
    query = "SELECT * FROM users;"
    cursor.execute(query)
    rows = cursor.fetchall()

    # Display each row under a filtered format
    for row in rows:
        filtered_data = "; ".join([f"{field}={formatter.REDACTION}" if\
                field in PII_FIELDS else f"{field}={value}" for field,\
                value in zip(cursor.column_names, row)])
        logger.info(filtered_data)

    # Close the cursor and connection
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
