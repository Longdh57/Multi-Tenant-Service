from starlette.testclient import TestClient

from tests.api import APITestCase


class TestGetStaffs(APITestCase):
    ISSUE_KEY = "O2OSTAFF-638"

    def test_get_staff_with_role_sale(self, client: TestClient):
        assert True

    def test_get_staff_with_role_sale_manager(self, client: TestClient):
        assert True

    def test_get_staff_with_role_sale_admin(self, client: TestClient):
        assert True

    def test_get_staff_with_role_team_lead(self, client: TestClient):
        assert True

    def test_get_staff_with_role_administrator(self, client: TestClient):
        assert True
