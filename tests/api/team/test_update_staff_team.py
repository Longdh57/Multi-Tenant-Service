import json

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from app.schemas.sche_base import ResponseSchemaBase
from tests.api import APITestCase


class TestCreateUpdateTeamApi(APITestCase):
    ISSUE_KEY = "O2OSTAFF-298"

    def test_000_response(self, client: TestClient):
        """
            Test Api put create/update staff in team response code 000
            Step by step:
            - Gọi API Create/Update Team với đầu vào chuẩn
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        assert True

    def test_001_response_field_values_cannot_empty(self, client: TestClient):
        """
            Test Api put create/update staff in team response code 001
            Step by step:
            - Gọi API Create/Update Team với param: field_values co chứa trường tìm kiếm không trong danh sách của document
            - Đầu ra mong muốn:
                . status code: 400
                . code: 001
        """
        assert True

    def test_004_response_field_values_invalid(self, client: TestClient):
        """
            Test Api put create/update staff in team response code 004
            Step by step:
            - Gọi API Create/Update Team với đầu vào chuẩn
            - Đầu ra mong muốn:
                . status code: 200
                . code: 004
        """
        assert True

    def test_134_response_staff_not_found(self, client: TestClient):
        """
            Test Api put create/update staff in team response code 134
            Step by step:
            - Gọi API Create/Update Team với đầu vào chuẩn
            - Đầu ra mong muốn:
                . status code: 200
                . code: 134
        """
        assert True

    def test_161_response_id_not_found(self, client: TestClient):
        """
            Test Api put create/update staff in team response code 000
            Step by step:
            - Gọi API Create/Update Team với đầu vào chuẩn
            - Đầu ra mong muốn:
                . status code: 200
                . code: 161
        """
        assert True

    def test_999_internal_error(self, client: TestClient):
        """
            Test Api put create/update staff in team response code 999
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
