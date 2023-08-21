import pytest
from accounts.dto.user_creation import UserCreationSchema, UserVerification, UserVerifyEmailSchema, UserReset, \
    UserResetSchema
from accounts.models.user import User


def test_valid_user_creation_schema():
    # Set up test data
    data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "Test1234",
        "phone": "1234567890",
        "address": "Test Address",
        "postalcode": "12345",
    }

    # Create schema object and validate data
    schema = UserCreationSchema()
    validated_data = schema.load(data)

    # Verify validated data
    assert validated_data["u_name"] == data["name"]
    assert validated_data["u_email"] == data["email"]
    assert validated_data["u_password"] == data["password"]
    assert validated_data["u_phone"] == data["phone"]
    assert validated_data["u_address"] == data["address"]
    assert validated_data["u_postalcode"] == data["postalcode"]


def test_invalid_user_creation_schema():
    # Set up test data
    data = {"name": "Test User", "email": "invalid", "password": "short", "phone": "1234567890",
            "address": "Test Address", "postalcode": "12345"}

    # Create schema object and validate data
    schema = UserCreationSchema()
    with pytest.raises(Exception):
        schema.load(data)


def test_valid_user_email_schema():
    # Set up test data
    data = {"username": "test@example.com", "otp": 1234}

    # Create schema object and validate data
    schema = UserVerifyEmailSchema()
    validated_data = schema.load(data)

    # Verify validated data
    assert validated_data["username"] == data["username"]
    assert validated_data["otp"] == data["otp"]


def test_invalid_user_email_schema_invalid():
    # Set up test data with missing required fields
    data = {
        'username': 'johndoe@example.com'
    }

    # Create schema object and verify that validation raises a ValidationError
    schema = UserVerifyEmailSchema()
    with pytest.raises(Exception):
        schema.load(data)


def test_valid_user_reset_schema():
    # Set up test data
    data = {"username": "test@example.com"}

    # Create schema object and validate data
    schema = UserResetSchema()
    validated_data = schema.load(data)

    # Verify validated data
    assert validated_data["username"] == data["username"]


def test_invalid_user_reset_schema():
    # Set up test data with missing required fields
    data = {}

    # Create schema object and verify that validation raises a ValidationError
    schema = UserResetSchema()
    with pytest.raises(Exception):
        schema.load(data)
