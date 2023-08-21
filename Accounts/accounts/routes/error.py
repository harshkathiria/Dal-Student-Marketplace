import traceback

from flask import Blueprint, jsonify
from werkzeug.exceptions import NotFound
from marshmallow import ValidationError

error_bp = Blueprint("errors", __name__)


@error_bp.app_errorhandler(NotFound)
def handler_not_found(error):
    print(traceback.format_exc())
    return jsonify({"message": "this resource isn't available"}, 404)


@error_bp.app_errorhandler(ValidationError)
def handle_invalid_data(error):
    print(traceback.format_exc())
    return jsonify({"message": "Incorrect format data"}), 400


@error_bp.app_errorhandler(Exception)
def handle_generic_exception(err):
    print(traceback.format_exc())
    return jsonify({"message": "Unknown error, Please check the logs"}), 500