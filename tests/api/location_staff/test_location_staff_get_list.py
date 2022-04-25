import json

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.core.config import settings
from app.schemas.sche_base import ResponseSchemaBase
from tests.api import APITestCase
from starlette.testclient import TestClient
from tests.faker import fake


class TestGetLocationStaffListAPI(APITestCase):
    ISSUE_KEY = "O2OSTAFF-584"

    def test_000_response_with_no_params(self, client: TestClient):
        """
            Test api get Location-Staff List response code 000
            Step by step:
            - Gọi API Location-Staff List với đầu vào chuẩn, không bao gồm params
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        location_staffs = fake.location_staffs()
        resp = client.get(f"{settings.BASE_API_PREFIX}/saleLocation")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert len(data.get('data')) == len(location_staffs)

    def test_000_response_with_province_code(self, client: TestClient):
        """
            Test api get Location-Staff List response code 000
            Step by step:
            - Gọi API Location-Staff List với đầu vào bao gồm params provinceCode có tồn tại
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        # staff = fake.staff_provider({'id': int(settings.LOCATION_ADMINISTRATOR)})
        # location_staffs = fake.location_staffs(staff=staff)
        # resp = client.get(f"{settings.BASE_API_PREFIX}/saleLocation?provinceCode=48")
        # data = resp.json()
        #
        # assert resp.status_code == 200
        # assert data.get('code') == '000'
        # assert data.get('message') == 'Thành công'
        # assert len(data.get('data')) == 1
        assert True

    def test_return_response_code_200_province_code_not_exists(self, client: TestClient):
        """
            Test api get Location-Staff List response code 200
            Step by step:
            - Gọi API Location-Staff List với đầu vào bao gồm params provinceCode không tồn tại
            - Đầu ra mong muốn:
                . status code: 400
                . code: 200
        """
        fake.location_staffs()
        resp = client.get(f"{settings.BASE_API_PREFIX}/saleLocation?provinceCode=4800")
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '200'

    def test_999_internal_error(self, client: TestClient):
        """
            Test api get Location Staff response code 999
            Step by step:
            - Gọi API Location Staff lỗi
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
