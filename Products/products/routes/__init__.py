from functools import wraps

import jwt
from flask import Flask, request, jsonify, current_app

app = Flask(__name__)


def authenticate_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        secret_key = current_app.config['HASH_SECRET']

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            token = auth_header

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
            print(decoded_token)
            kwargs['decoded_token'] = decoded_token
            return f(*args, **kwargs)
        except jwt.exceptions.InvalidTokenError:
            return jsonify({'message': 'Token is invalid'}), 401

    return decorated
