from flask import Blueprint

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health_check():
    return "Accounts app working ok"  # defined a health check endpoint for testing
