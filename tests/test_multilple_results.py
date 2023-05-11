from the_one_api._base._base import Endpoint
from the_one_api._base._multiple_results import Filter, MultipleObjectsMixin


class ListableEndpoint(MultipleObjectsMixin, Endpoint):
    requires_auth = False
    endpoint = "valid/"


def test_parse_sort():
    """
    Test the parse_sort method of the Filter class
    """
    param1 = Filter(sort="name").query_params
    param2 = Filter(sort="-name").query_params

    assert param1 == "sort=name:asc"
    assert param2 == "sort=name:desc"


def test_parse_match():
    """Test the parse_match method of the Filter class"""

    param = Filter(match={"name": "foo"}).query_params

    assert param == "name=foo"


def test_parse_negate_match():
    """Test the parse_negate_match method of the Filter class"""

    param = Filter(negate_match={"score": 100}).query_params

    assert param == "score!=100"


def test_parse_filter():
    """Test the parse_filter method of the Filter class"""

    param = Filter(filter={"name": ["foo", "bar"]}).query_params

    assert param == "name=foo,bar"


def test_parse_exclude():
    """Test the parse_exclude method of the Filter class"""

    param = Filter(exclude={"name": ["foo", "bar"]}).query_params

    assert param == "name!=foo,bar"


def test_parse_regex():
    """Test the parse_regex method of the Filter class"""

    param = Filter(regex={"name": "/foo/i"}).query_params

    assert param == "name=/foo/i"


def test_parse_negate_regex():
    """Test the parse_negate_regex method of the Filter class"""

    param = Filter(negate_regex={"name": "/foo/i"}).query_params

    assert param == "name!=/foo/i"


def test_parse_lt():
    """Test the parse_lt method of the Filter class"""

    param1 = Filter(lt={"name": "B"}).query_params
    param2 = Filter(lt={"score": 100}).query_params

    assert param1 == "name<B"
    assert param2 == "score<100"


def test_parse_gt():
    """Test the parse_gt method of the Filter class"""

    param1 = Filter(gt={"name": "B"}).query_params
    param2 = Filter(gt={"score": 100}).query_params

    assert param1 == "name>B"
    assert param2 == "score>100"


def test_parse_gte():
    """Test the parse_gte method of the Filter class"""

    param1 = Filter(gte={"name": "B"}).query_params
    param2 = Filter(gte={"score": 100}).query_params

    assert param1 == "name>=B"
    assert param2 == "score>=100"


def test_filter_query_params_with_multiple_params():
    """Test the query_params Filter property when multiple params are involved."""

    param = Filter(gt={"score": 10}, lt={"score": 100}).query_params
    params = param.split("&")

    assert len(params) == 2
    assert "score>10" in params
    assert "score<100" in params


def test_list_all(mocker, mock_response):
    """Test the MultipleObjectsMixin's 'list_all' method when the requested objects
    are found."""

    mock_get = mocker.patch("requests.get")
    data = {
        "docs": [
            {"_id": "asdfasdfasdf", "name": "Thing 1", "runtimeInMinutes": 200},
            {"_id": "qwerqwerqwer", "name": "Thing 2", "runtimeInMinutes": 250},
        ]
    }
    mock_get.return_value = mock_response(status_code=200, contents=data)

    results = ListableEndpoint().list_all()

    assert len(results) == 2


def test_filter(mocker, mock_response):
    """Test the MultipleObjectsMixin's 'filter' method when the requested objects
    are found."""

    mock_get = mocker.patch("requests.get")
    data = {
        "docs": [
            {"_id": "asdfasdfasdf", "name": "Thing 1", "runtimeInMinutes": 200},
            {"_id": "qwerqwerqwer", "name": "Thing 2", "runtimeInMinutes": 250},
            {"_id": "zxcvzxcvzxcv", "name": "Thing 3", "runtimeInMinutes": 300},
        ]
    }
    mock_get.return_value = mock_response(status_code=200, contents=data)

    results = ListableEndpoint().filter(sort="name", gte={"runtimeInMinutes": 200})

    assert len(results) == 3
