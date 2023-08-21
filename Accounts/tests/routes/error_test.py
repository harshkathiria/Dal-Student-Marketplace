from unittest import mock
from unittest.mock import patch
from flask import Flask, jsonify
from werkzeug.exceptions import NotFound
from marshmallow import ValidationError
from accounts.routes.error import error_bp, handle_generic_exception
import json

def test_handler_not_found(client):
    # Simulate a request to a nonexistent endpoint
    response = client.get("/nonexistent")

    # Verify response status code and message
    assert response.status_code == 404
    assert response.json == {"message": "this resource isn't available"}


def test_handle_invalid_data(client):
    # Simulate a request with invalid data
    response = client.post("/endpoint", json={'invalid_field': "value"})

    # Verify response status code and message
    assert response.status_code == 400
    assert response.json == {"message": "Incorrect format data"}


def test_handle_generic_exception():
    # Simulate a generic exception being raised
    with patch("builtins.print") as mock_print:
        with Flask(__name__).test_request_context():
            response = handle_generic_exception(Exception("Something went wrong"))

    # Verify response status code and message
    assert response.status_code == 500
    assert response.json == {"message": "Unknown error, Please check the logs"}

    # Verify that the exception was logged
    mock_print.assert_called_once_with(mock.ANY)
