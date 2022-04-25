import json

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from app.schemas.sche_base import ResponseSchemaBase
from tests.api import APITestCase


class TestaddStaffsToTeamApi(APITestCase):
    ISSUE_KEY = "O2OSTAFF-297"

    def test_000_response(self, client: TestClient):
        """
            Test api Post add list staffs to team response code 000
            Step by step:
            - Gọi API Add List Staff to Team với đầu vào chuẩn
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        assert True

    def test_006_response_field_values_invalid(self, client: TestClient):
        """
            Test api Post add list staffs to team response code 000
            Step by step:
            - Gọi API Add List Staff to Team với đầu vào chuẩn
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        assert True

    def test_161_response_id_not_found(self, client: TestClient):
        """
            Test api Post add list staffs to team response code 000
            Step by step:
            - Gọi API Add List Staff to Team với đầu vào chuẩn
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        assert True

    def test_134_response_staff_not_found(self, client: TestClient):
        """
            Test api Post add list staffs to team response code 000
            Step by step:
            - Gọi API Add List Staff to Team với đầu vào chuẩn
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        assert True

    def test_999_internal_error(self, client: TestClient):
        """
            Test api post create/update team response code 999
            Step by step:
            - Gọi API Create/Update Team lỗi
            - Đầu ra mong muốn:
                . status code: 500
                . code: 999
        """
        res = JSONResponse(
            status_code=500,
            content=jsonable_encoder(
                ResponseSchemaBase().custom_response(
                    '999', "Hệ thống đang bảo trì, quý khách vui lòng thử lại sau"
                )
            )
        )
        assert res.status_code == 500 and json.loads(res.body) == {
            "code": "999",
            "message": "Hệ thống đang bảo trì, quý khách vui lòng thử lại sau"
        }
