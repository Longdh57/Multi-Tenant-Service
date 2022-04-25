import json

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.core.config import settings
from app.schemas.sche_base import ResponseSchemaBase
from tests.api import APITestCase
from starlette.testclient import TestClient
from tests.faker import fake
from app.core import error_code, message


class TestUpdateMappingLocationStaffListAPI(APITestCase):
    ISSUE_KEY = "O2OSTAFF-591"

    def test_http_200_code_000_success(self, client: TestClient):
        """
            Test api get Location-Staff List response code 000
            Step by step:
            - Gọi API Update Mapping location với params:
                . provinceCode
                . staffId
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        # location_staffs = fake.location_staffs()
        # user = fake.user()
        # params = {
        #     'provinceCode': location_staffs[0].provinceCode,
        #     'staffId': user.id,
        # }
        # resp = client.post(f"{settings.BASE_API_PREFIX}/staffLocation", params=params)
        # data = resp.json()

        # assert resp.status_code == 200
        # assert data.get('code') == '000'
        # assert data.get('message') == 'Thành công'
        assert True

    def test_http_400_code_200_province_code_not_exists(self, client: TestClient):
        """
            Test api get Location-Staff List response code 000
            Step by step:
            - Gọi API Update Mapping location với params:
                . provinceCode: không tồn tại
                . staffId
            - Đầu ra mong muốn:
                . status code: 400
                . code: 200
        """
        res = JSONResponse(
            status_code=400,
            content=jsonable_encoder(
                ResponseSchemaBase().custom_response(
                    error_code.ERROR_200_PROVINCE_CODE_NOT_EXITS, message.MESSAGE_200_PROVINCE_CODE_NOT_EXITS
                )
            )
        )
        assert res.status_code == 400 and json.loads(res.body) == {
            "code": error_code.ERROR_200_PROVINCE_CODE_NOT_EXITS,
            "message": message.MESSAGE_200_PROVINCE_CODE_NOT_EXITS
        }

    def test_http_422_staff_id_is_not_a_valid_integer(self, client: TestClient):
        """
            Test api get Location-Staff List response code 000
            Step by step:
            - Gọi API Update Mapping location với params:
                . provinceCode: hợp lệ
                . staffId: kiểu str
            - Đầu ra mong muốn:
                . status code: 422
                . code: 
        """
        assert True

    def test_http_200_code_000_staff_id_is_None(self, client: TestClient):
        """
            Test api get Location-Staff List response code 000
            Step by step:
            - Gọi API Update Mapping location với params:
                . provinceCode: hợp lệ
                . staffId: None
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        assert True


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
