from multiprocessing import AuthenticationError

import jwt
from flask import Blueprint, request, jsonify
from flask import current_app
from werkzeug.security import check_password_hash

from accounts import db
from accounts.dto.credentials import CredentialsSchema
from accounts.models.user import User

auth_bp = Blueprint("auth", __name__)
credentials_schema = CredentialsSchema()


@auth_bp.route("/login", methods=["POST"])
def login():
    d = request.json
    credentials = credentials_schema.load(d)
    secret_token = current_app.config['HASH_SECRET']
    if not credentials.username or not credentials.password:
        raise ValueError("Unable to authenticate")
        # if either username/password not available in request throw exception

    user = db.session.query(User).filter_by(u_email=credentials.username).first()
    if not user or not check_password_hash(
            user.u_password,
            credentials.password
    ):
        raise AuthenticationError("Invalid username or Password")
    if not user.u_emailVerified:
        return jsonify({"message": "Email not Verified"})
    else:
        encoded_jwt = jwt.encode(
            {"name": user.u_name,
             "username": user.u_email,
             "user_id": user.u_id},
            secret_token,
            algorithm="HS256")
        return jsonify({"token": encoded_jwt})
# referenced from https://pyjwt.readthedocs.io/en/latest/usage.html

