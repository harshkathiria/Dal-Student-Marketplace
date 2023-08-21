import os

import jwt

from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from sqlalchemy import select
from werkzeug.security import check_password_hash, generate_password_hash

from accounts import db
from accounts.models.user import User
from flask import current_app

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme="Bearer")


@basic_auth.verify_password
def verify_basic_password(username, password):
    user = db.session.scalars(select(User).where(User.u_email == username)).one_or_none()
    if not user:
        return None
    if check_password_hash(user.u_password, password):
        return username


@token_auth.verify_token
def verify_token(token):
    secret_token = current_app.config['HASH_SECRET']
    try:
        decoded_jwt = jwt.decode(
                            token,
                            secret_token,
                            algorithms=["HS256"])
    except Exception as ex:
        print(ex)
        return None

    user = db.session.scalars(select(User).where(User.u_email == decoded_jwt["username"])).one_or_none()

    if user:
        return decoded_jwt["username"]
    return None
