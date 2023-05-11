from the_one_api._base._base import Endpoint
from the_one_api._base._single_results import SingleObjectsMixin


class MockObject(SingleObjectsMixin, Endpoint):
    requires_auth = False
    endpoint = "valid/"


def test_single_results_mixin_get_success(mocker, mock_response):
    """
    Test the SingleObjectsMixin's 'get' method when the requested object is found.
    """
    mock_get = mocker.patch("requests.get")
    obj_id = "5cd95395de30eff6ebccde5b"
    data = {
        "docs": [
            {
                "_id": obj_id,
                "name": "The Two Towers",
                "runtimeInMinutes": 179,
                "budgetInMillions": 94,
                "boxOfficeRevenueInMillions": 926,
                "academyAwardNominations": 6,
                "academyAwardWins": 2,
                "rottenTomatoesScore": 96,
            }
        ],
        "total": 1,
        "limit": 1000,
        "offset": 0,
        "page": 1,
        "pages": 1,
    }
    mock_get.return_value = mock_response(status_code=200, contents=data)

    result = MockObject().get(obj_id)

    assert result
    assert result.get("_id") == obj_id
    assert result.get("name") == "The Two Towers"
    assert result.get("runtimeInMinutes") == 179
    assert result.get("budgetInMillions") == 94
    assert result.get("boxOfficeRevenueInMillions") == 926
    assert result.get("academyAwardNominations") == 6
    assert result.get("academyAwardWins") == 2
    assert result.get("rottenTomatoesScore") == 96


def test_single_results_mixin_get_not_found(mocker, mock_response):
    """
    Test the SingleObjectsMixin's 'get' method when the requested object is not found.
    """
    mock_get = mocker.patch("requests.get")
    obj_id = "4cd95395de30eff6ebccde5b"
    data = {"docs": [], "total": 0, "limit": 1000, "offset": 0, "page": 1, "pages": 1}
    mock_get.return_value = mock_response(status_code=200, contents=data)

    result = MockObject().get(obj_id)

    assert result is None
