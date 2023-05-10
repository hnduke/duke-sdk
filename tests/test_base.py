import pytest

import the_one_api
from the_one_api._base._base import Endpoint


class NoAuthRequiredEndpoint(Endpoint):
    pass


class AuthRequiredEndpoint(Endpoint):
    requires_auth = True


class MockHTTPResponse:
    def __init__(self, status_code: int, contents: dict):
        self.status_code = status_code
        self.contents = contents
        self.ok = True if 200 <= status_code <= 399 else False

    def json(self):
        return self.contents


def test_endpoint_no_auth_required_success(mocker):
    """
    Test successful request to an endpoint that does not require authentication.
    """

    mock_get = mocker.patch("requests.get")
    mock_get.return_value = MockHTTPResponse(
        status_code=200, contents={"success": "true"}
    )

    endpoint = NoAuthRequiredEndpoint()
    response = endpoint._make_request("valid_endpoint")

    assert isinstance(response, dict)
    assert "success" in response
    assert response["success"] == "true"


def test_endpoint_auth_required_success(mocker):
    """
    Test successful request to an endpoint that requires authentication.
    """
    mocker.patch("the_one_api.api_key", new="test-api-key")
    mock_get = mocker.patch("requests.get")
    mock_get.return_value = MockHTTPResponse(
        status_code=200, contents={"success": "true"}
    )

    endpoint = AuthRequiredEndpoint()
    response = endpoint._make_request("valid_endpoint")

    assert isinstance(response, dict)
    assert "success" in response
    assert response["success"] == "true"


def test_endpoint_auth_required_missing_api_key(mocker):
    """
    Test request to an endpoint that requires authentication but API key is missing.
    """
    # api_key is None by default
    mock_get = mocker.patch("requests.get")
    mock_get.return_value = MockHTTPResponse(
        status_code=401, contents={"success": "false", "message": "Unauthorized."}
    )

    endpoint = AuthRequiredEndpoint()
    with pytest.raises(the_one_api.errors.APIError) as e:
        endpoint._make_request("valid_endpoint")

    assert "Unauthorized" in e.value.args[0]


def test_endpoint_auth_required_incorrect_api_key(mocker):
    """
    Test request to an endpoint that requires authentication but API key is incorrect.
    """
    mocker.patch("the_one_api.api_key", new="wrong-api-key")
    mock_get = mocker.patch("requests.get")
    mock_get.return_value = MockHTTPResponse(
        status_code=401, contents={"success": "false", "message": "Unauthorized."}
    )

    endpoint = AuthRequiredEndpoint()
    with pytest.raises(the_one_api.errors.APIError) as e:
        endpoint._make_request("valid_endpoint")

    assert "Unauthorized" in e.value.args[0]


def test_endpoint_auth_required_correct_key_but_endpoint_does_not_exist(mocker):
    """
    Test request to an endpoint that requires authentication, API key is correct,
    but server returns an error response.
    """
    mocker.patch("the_one_api.api_key", new="test-api-key")
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.status_code = 404
    mock_get.return_value = MockHTTPResponse(
        status_code=404,
        contents={"success": "false", "message": "Endpoint does not exist."},
    )

    endpoint = AuthRequiredEndpoint()
    with pytest.raises(the_one_api.errors.APIError) as e:
        endpoint._make_request("valid_endpoint")

    assert "Endpoint does not exist" in e.value.args[0]


def test_endpoint_auth_required_correct_key_but_server_error_response(mocker):
    """
    Test request to an endpoint that requires authentication, API key is correct,
    but server returns an error response.
    """
    mocker.patch("the_one_api.api_key", new="test-api-key")
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.status_code = 500
    mock_get.return_value = MockHTTPResponse(
        status_code=404,
        contents={"success": "false", "message": "System-dependent error message"},
    )

    endpoint = AuthRequiredEndpoint()
    with pytest.raises(the_one_api.errors.APIError):
        endpoint._make_request("valid_endpoint")
