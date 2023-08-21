from marshmallow import Schema, fields, post_load, validates, ValidationError
import re


class Credentials:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class CredentialsSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

    @validates("username")
    def validates_email(self, value):
        if not re.match("[^@]+@[^@]+\.[^@]+", value):
            raise ValidationError("Invalid username format")

    @validates("password")
    def validates_password(self, value):
        if len(value) < 8:
            raise ValidationError("Password must longer than 8")
        if not any(char.isupper() for char in value):
            raise ValidationError("Password must contain upper case")
        if not any(char.islower() for char in value):
            raise ValidationError("Password must contain lower case")

    @post_load
    def make_credentials(self, data, **kwargs):
        return Credentials(**data)
