import pytest


@pytest.fixture
def mock_response():
    class MockHTTPResponse:
        def __init__(self, status_code: int, contents: dict):
            self.status_code = status_code
            self.contents = contents
            self.ok = True if 200 <= status_code <= 399 else False

        def json(self):
            return self.contents

    return MockHTTPResponse
