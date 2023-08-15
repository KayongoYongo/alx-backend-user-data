#!/usr/bin/env python3
"""Basic flask app
"""
from auth import Auth
from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index() -> str:
    """Returns a simple JSONIFY request
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

