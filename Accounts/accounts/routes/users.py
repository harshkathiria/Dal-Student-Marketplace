from sqlalchemy import select, insert, update
from werkzeug.security import generate_password_hash

from accounts import db
from accounts.dto.user_creation import UserCreationSchema, UserVerifyEmailSchema, UserResetSchema
from accounts.emailsend import email_send
from accounts.generateOTP import generate_otp
from accounts.models.user import User, UserSchema
from flask import Blueprint, jsonify, request, Response

from accounts.passwordGenerator import generate_password
from accounts.routes import token_auth

users_bp = Blueprint("users", __name__, url_prefix="/users")
user_schema = UserSchema()
user_creation_schema = UserCreationSchema()
user_email_verify = UserVerifyEmailSchema()
user_reset = UserResetSchema()


@users_bp.route("", methods=["GET"])
@token_auth.login_required
def get_all_users():
    users = db.session.scalars(select(User)).all()
    return jsonify(user_schema.dump(users, many=True))


@users_bp.route("/signup", methods=["POST"])
def create_user():
    d = request.json
    new_user = user_creation_schema.load(d)
    otp = generate_otp()

    db.session.execute(
        insert(User).values(
            u_name=new_user.u_name,
            u_email=new_user.u_email,
            u_password=generate_password_hash(new_user.u_password),
            u_phone=new_user.u_phone,
            u_address=new_user.u_address,
            u_postalcode=new_user.u_postalcode,
            u_otp=otp,
            u_emailVerified=0  # set default value to zero
        ))
    db.session.commit()
    email_send(new_user.u_name, new_user.u_email, otp)
    return Response(status=204)


@users_bp.route("/get_user", methods=["GET"])
@token_auth.login_required
def get_user():
    current_user_email = token_auth.current_user()
    user = db.session.scalars(select(User).where(User.u_email == current_user_email)).one()
    return jsonify(user_schema.dump(user))

@users_bp.route("/get_seller/<user_id>", methods=["GET"])
@token_auth.login_required
def get_seller(user_id):
    user = db.session.scalars(select(User).where(User.u_id == user_id)).one()
    return jsonify(user_schema.dump(user))

@users_bp.route("/verify_email", methods=["POST"])
def verify_email():
    d = request.json
    email_verify = user_email_verify.load(d)
    user = db.session.scalars(select(User).where(User.u_email == email_verify.username)).one()
    if user.u_otp == email_verify.otp:
        db.session.execute((update(User).
                            where(User.u_email == user.u_email).
                            values(u_emailVerified=True, u_otp=None)))
        db.session.commit()
        return Response(status=204)
    else:
        return Response(status=400)

@users_bp.route("/reset", methods=["POST"])
def reset_user():
    d = request.json
    reset = user_reset.load(d)
    password = generate_password()
    user = db.session.scalars(select(User).where(User.u_email == reset.username)).one()
    name = user.u_name

    db.session.execute((update(User).
                        where(User.u_email == reset.username).
                        values(u_password=generate_password_hash(password))))
    db.session.commit()
    # send the email
    email_send(name, reset.username, password)
    return Response(status=204)

