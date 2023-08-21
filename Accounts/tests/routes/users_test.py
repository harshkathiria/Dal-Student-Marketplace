import pytest
from unittest.mock import Mock, patch
from werkzeug.security import generate_password_hash
from sqlalchemy import select
from accounts.models.user import User
from accounts.routes import users
from accounts.passwordGenerator import generate_password

username = "test@example.com"

@pytest.fixture(scope="module")
def client():
    with users.test_client() as client:
        with users.app_context():
            yield client


@patch("accounts.emailsend.email_send")
def test_create_user(mock_email_send, client):
    data = {
        "u_name": "test",
        "u_email": "test@example.com",
        "u_password": "Test@12345",
        "u_phone": "1234567890",
        "u_address": "Test Address",
        "u_postalcode": "123456",
    }
    response = client.post("/users/signup", json=data)
    assert response.status_code == 204
    assert mock_email_send.called


def test_create_user_with_invalid_data(client):
    data = {
        "u_name": "",
        "u_email": "test@example.com",
        "u_password": "test1234",
        "u_phone": "1234567890",
        "u_address": "Test Address",
        "u_postalcode": "123456",
    }
    response = client.post("/users/signup", json=data)
    assert response.status_code == 422


def test_get_all_users(client):
    response = client.get("/users")
    assert response.status_code == 200


def test_get_user(client):
    response = client.get(f"/users/{username}")
    assert response.status_code == 200


@patch("accounts.emailsend.email_send")
def test_reset_user(mock_email_send, client):
    data = {"username": username}
    response = client.post("/users/reset", json=data)
    assert response.status_code == 204
    assert mock_email_send.called


def test_verify_email(client):
    data = {"username": username, "otp": "123456"}
    response = client.post("/users/verify_email", json=data)
    assert response.status_code == 204


def test_verify_email_with_invalid_otp(client):
    data = {"username": username, "otp": "123"}
    response = client.post("/users/verify_email", json=data)
    assert response.status_code == 400


def test_generate_password():
    password = generate_password()
    assert len(password) == 8


def test_generate_password_hash():
    password = "Test@12345"
    password_hash = generate_password_hash(password)
    assert len(password_hash) > 0


def test_select_user():

    query = select(User).where(User.u_email == username)
    assert str(query) == "SELECT users.u_id, users.u_name, users.u_email, users.u_password, users.u_phone, " \
                         "users.u_address, users.u_postalcode, users.u_otp, users.u_emailVerified, users.u_created_at, " \
                         "users.u_updated_at \nFROM users \nWHERE users.u_email = :u_email_1"
