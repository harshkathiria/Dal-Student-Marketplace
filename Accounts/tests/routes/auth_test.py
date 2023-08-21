# import pytest
# from unittest.mock import patch
# from accounts import db, create_app
# from accounts.dto.credentials import CredentialsSchema
from accounts.models.user import User
# from werkzeug.security import generate_password_hash
#
#
# @pytest.fixture
# def client():
#     app = create_app({"TESTING": True})
#     with app.test_client() as client:
#         with app.app_context():
#             db.create_all()
#             yield client
#             db.drop_all()
#
#
# @pytest.fixture
# def mock_user():
#     user = User(u_name='Test User', u_email='test@example.com', u_password=generate_password_hash('Test1234'))
#     db.session.add(user)
#     db.session.commit()
#     yield user
#     db.session.delete(user)
#     db.session.commit()
#
#
# def test_login_with_valid_credentials(client, mock_user, monkeypatch):
#     credentials = {'username': mock_user.u_email, 'password': 'Test1234'}
#     with patch('accounts.views.auth.current_app') as mock_app:
#         mock_app.config = {'HASH_SECRET': 'test-secret'}
#         response = client.post('/login', json=credentials)
#
#     assert response.status_code == 200
#     assert 'token' in response.json
#
#
# def test_login_with_invalid_credentials(client, mock_user, monkeypatch):
#     credentials = {'username': mock_user.u_email, 'password': 'WrongPassword'}
#     with patch('accounts.views.auth.current_app') as mock_app:
#         mock_app.config = {'HASH_SECRET': 'test-secret'}
#         response = client.post('/login', json=credentials)
#
#     assert response.status_code == 500
#     assert response.json['message'] == 'Invalid username or Password'
#
#
# def test_login_with_unverified_email(client, mock_user, monkeypatch):
#     mock_user.u_emailVerified = False
#     db.session.commit()
#
#     credentials = {'username': mock_user.u_email, 'password': 'Test1234'}
#     with patch('accounts.views.auth.current_app') as mock_app:
#         mock_app.config = {'HASH_SECRET': 'test-secret'}
#         response = client.post('/login', json=credentials)
#
#     assert response.status_code == 200
#     assert response.json['message'] == 'Email not Verified'
#
#
# def test_login_with_missing_username(client):
#     credentials = {'password': 'Test1234'}
#     with patch('accounts.views.auth.current_app') as mock_app:
#         mock_app.config = {'HASH_SECRET': 'test-secret'}
#         response = client.post('/login', json=credentials)
#
#     assert response.status_code == 500
#     assert response.json['message'] == 'Unable to authenticate'
#
#
# def test_login_with_missing_password(client):
#     credentials = {'username': 'test@example.com'}
#     with patch('accounts.views.auth.current_app') as mock_app:
#         mock_app.config = {'HASH_SECRET': 'test-secret'}
#         response = client.post('/login', json=credentials)
#
#     assert response.status_code == 500
#     assert response.json['message'] == 'Unable to authenticate'
#
#
# def test_login_with_missing_credentials(client):
#     credentials = {}
#     with patch('accounts.views.auth.current_app') as mock_app:
#         mock_app.config = {'HASH_SECRET': 'test-secret'}
#         response = client.post('/login', json=credentials)
#
#     assert response.status_code == 500
#     assert response.json['message'] == 'Unable to authenticate'
#
#
# def test_login_with_invalid_username_format(client):
#     credentials = {'username': 'testexample.com', 'password': 'Test1234'}
#     with patch('accounts.views.auth.current_app') as mock_app:
#         mock_app.config = {'HASH_SECRET': 'test-secret'}
#         response = client.post('/login', json=credentials)
#
#     assert response.status_code == 422
#     assert 'Invalid username format' in response.json['message']['username']
#
#
# def test_login_with_short_password(client):
#     credentials = {'username': 'test@example.com', 'password': 'Test123'}
#     with patch('accounts.views.auth.current_app') as mock_app:
#         mock_app.config = {'HASH_SECRET': 'test-secret'}
#         response = client.post('/login', json=credentials)
#
#     assert response.status_code == 422
#     assert 'Password must longer than 8' in response.json['message']['password']

import jwt
from flask import current_app
from werkzeug.security import generate_password_hash

from accounts.dto.credentials import Credentials

user_name = "Test User"
user_email = "test@test.com"
user_password = "password"


def test_login_successful(client, mocker):
    # create a test user with a password

    hashed_password = generate_password_hash(user_password)

    user = User(u_email=user_email, u_password=hashed_password, u_emailVerified=True, u_name=user_name)

    db_session_mock = mocker.patch("accounts.auth.db.session")
    db_session_mock.query.return_value.filter_by.return_value.first.return_value = user

    credentials = Credentials(username=user_email, password=user_password)

    mocker.patch.object(current_app.config, 'HASH_SECRET', 'test-secret')

    expected_token = jwt.encode(
        {"name": user.u_name, "username": user.u_email, "user_id": user.u_id},
        "test-secret",
        algorithm="HS256"
    )
    response = client.post("/login", json=credentials.to_dict())
    assert response.status_code == 200
    assert response.json["token"] == expected_token


def test_login_missing_username(client):
    credentials = Credentials(username=None, password="password")
    response = client.post("/login", json=credentials.to_dict())
    assert response.status_code == 400
    assert "Unable to authenticate" in response.json["message"]


def test_login_missing_password(client):
    credentials = Credentials(username=user_email, password=None)
    response = client.post("/login", json=credentials.to_dict())
    assert response.status_code == 400
    assert "Unable to authenticate" in response.json["message"]


def test_login_invalid_credentials(client, mocker):
    # create a test user with a password
    hashed_password = generate_password_hash(user_password)
    user = User(u_email=user_email, u_password=hashed_password, u_emailVerified=True, u_name=user_name)
    db_session_mock = mocker.patch("accounts.auth.db.session")
    db_session_mock.query.return_value.filter_by.return_value.first.return_value = None
    credentials = Credentials(username=user_email, password=user_password)
    response = client.post("/login", json=credentials.to_dict())
    assert response.status_code == 401
    assert "Invalid username or Password" in response.json["message"]


def test_login_unverified_email(client, mocker):
    # create a test user with a password
    hashed_password = generate_password_hash(user_password)
    user = User(u_email=user_email, u_password=hashed_password, u_emailVerified=False, u_name=user_name)
    db_session_mock = mocker.patch("accounts.auth.db.session")
    db_session_mock.query.return_value.filter_by.return_value.first.return_value = user
    credentials = Credentials(username=user_email, password=user_password)
    response = client.post("/login", json=credentials.to_dict())
    assert response.status_code == 200
    assert "Email not Verified" in response.json["message"]
