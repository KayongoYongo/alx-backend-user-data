#!/usr/bin/env python3
"""Basic flask app
"""
from auth import Auth
from flask import Flask, jsonify, request, abort, redirect


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

    if not AUTH.valid_login(email, password):
        abort(401)
    else:
        # if the form data is correct
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)

    return response


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """This function impliments a log out function by
    deleting a session

    Args:
        None

    Return:
        Redirect request
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """
    This functon impliments a get profile function

    Args:
        None

    Return:
        user
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> str:
    """
    This function gets the reset password token.

    Args:
        None

    Return:
        Response
    """
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
