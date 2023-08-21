from unittest import mock
from accounts.routes.health import health_bp


def test_health_check_endpoint(client):
    # Make a GET request to the health check endpoint
    response = client.get("/health")

    # Verify response status code and data
    assert response.status_code == 200
    assert response.data == b"Accounts app working ok"


@mock.patch("app.health_bp.route")
def test_health_check_route(mock_route):
    # Call the health_check function and verify it adds the expected route
    health_check = mock_route.return_value
    health_bp = mock.MagicMock()
    health_check(health_bp)

    mock_route.assert_called_once_with("/health", methods=["GET"])
    health_bp.add_url_rule.assert_called_once_with("/health", view_func=health_check)
