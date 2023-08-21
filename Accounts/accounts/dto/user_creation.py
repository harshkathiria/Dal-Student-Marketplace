from marshmallow import Schema, fields, post_load

from accounts.models.user import User


class UserCreationSchema(Schema):
    name = fields.String(required=True, attribute='u_name', description='The Name of user')
    email = fields.String(required=True, attribute='u_email', description='Email address of user')
    password = fields.String(required=True, attribute='u_password', description='Password')
    phone = fields.String(required=True, attribute='u_phone', description='Phone number')
    address = fields.String(required=True, attribute='u_address', description='User Address')
    postalcode = fields.String(required=True, attribute='u_postalcode', description='Postal code of User')

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


class UserVerification:
    def __init__(self, username, otp):
        self.username = username
        self.otp = otp


class UserVerifyEmailSchema(Schema):
    username = fields.String(required=True)
    otp = fields.Integer(required=True)

    @post_load
    def verify_user(self, data, **kwargs):
        return UserVerification(**data)


class UserReset:
    def __init__(self, username):
        self.username = username


class UserResetSchema(Schema):
    username = fields.String(required=True)

    @post_load
    def reset_user(self, data, **kwargs):
        return UserReset(**data)

