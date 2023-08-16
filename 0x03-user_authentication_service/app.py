#!/usr/bin/env python3
"""Basic flask app
"""
from auth import Auth
from flask import Flask, jsonify, request


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def index() -> str:
    """Returns a simple JSONIFY request
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> str:
    """A function that impiments a POST method on the users table.

    Args:
        None

    Return:
        Return: A jsonify message
    """
    email = request.form.get('email')
    password = request.form.get('password')

    # register user if user does not exist
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """A function theat impliments a log in functionality

    Args:
        None

    Return:
        A JSONIFY message and return response
    """
    # Get the form data
    email = request.form.get('email')
    password = request.form.get('password')

    if not (AUTH.valid_login(email, password)):
        abort(401)
    else:
        # if the form data is correct
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)

     return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
