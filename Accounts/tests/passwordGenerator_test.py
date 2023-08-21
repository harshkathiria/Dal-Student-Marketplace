import pytest
from accounts.passwordGenerator import generate_password

# def test_generate_password_length():
#     # Ensure password is of correct length
#     password = generate_password()
#     assert len(password) == 8
#
#
# def test_generate_password_characters():
#     # Ensure password contains only valid characters
#     password = generate_password()
#     valid_characters = string.ascii_letters + string.digits + string.punctuation
#     assert all(char in valid_characters for char in password)
import random

length = 8


def test_generate_password_default_length():
    password = generate_password()
    assert isinstance(password, str)
    assert len(password) == 8


def test_generate_password_custom_length():
    password = generate_password(length=12)
    assert isinstance(password, str)
    assert len(password) == 12


def test_generate_password_invalid_length():
    with pytest.raises(ValueError):
        generate_password(length=-1)


def test_generate_password_randomness():
    password_1 = generate_password()
    password_2 = generate_password()
    assert password_1 != password_2
