import pytest
from accounts.dto.credentials import Credentials, CredentialsSchema, ValidationError
from marshmallow import ValidationError


@pytest.fixture
def valid_credentials_data():
    return {"username": "user@example.com", "password": "password123"}


@pytest.fixture
def invalid_credentials_data():
    return {"username": "invalid-email", "password": "weak"}


def test_credentials_schema_loads_valid_data(valid_credentials_data):
    schema = CredentialsSchema()
    credentials = schema.load(valid_credentials_data)
    assert isinstance(credentials, Credentials)
    assert credentials.username == valid_credentials_data["username"]
    assert credentials.password == valid_credentials_data["password"]


def test_credentials_schema_raises_validation_error_for_invalid_email(invalid_credentials_data):
    schema = CredentialsSchema()
    with pytest.raises(ValidationError) as exc_info:
        schema.load(invalid_credentials_data)
    assert "Invalid username format" in str(exc_info.value)


def test_credentials_schema_raises_validation_error_for_weak_password(invalid_credentials_data):
    schema = CredentialsSchema()
    with pytest.raises(ValidationError) as exc_info:
        schema.load(invalid_credentials_data)
    assert "Password must longer than 8" in str(exc_info.value)
    assert "Password must contain upper case" in str(exc_info.value)
    assert "Password must contain lower case" in str(exc_info.value)


def test_credentials_schema_dump(valid_credentials_data):
    credentials = Credentials(**valid_credentials_data)
    schema = CredentialsSchema()
    result = schema.dump(credentials)
    assert result == valid_credentials_data


def test_credentials_schema_post_load(valid_credentials_data):
    schema = CredentialsSchema()
    credentials = schema.load(valid_credentials_data)
    assert isinstance(credentials, Credentials)

