import pytest

from tests.conftest import Jira


@pytest.mark.usefixtures('app_class')
class APITestCase(Jira):
    pass


class MockResponse:
    def __init__(self, text, status_code):
        self.text = text
        self.status_code = status_code
