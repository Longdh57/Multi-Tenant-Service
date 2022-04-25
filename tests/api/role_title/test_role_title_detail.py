import json

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from app.core.config import settings
from app.schemas.sche_base import ResponseSchemaBase
from tests.api import APITestCase
from tests.faker import fake


class TestGetRoleTitleDetailAPI(APITestCase):
    ISSUE_KEY = "O2OSTAFF-289"

    def test_000_response_none_department(self, client: TestClient):
        """
            Test api get Role Title Detail response code 000
            Step by step:
            - Tạo company trên DB
            - Tạo role title gắn với company và không có department trên DB
            - Gọi API Role Title Detail với đầu vào chuẩn
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        role_title = fake.role_title_provider({'company_id': company.id, 'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/role_titles/{role_title.id}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['id'] == role_title.id

    def test_000_response_with_department(self, client: TestClient):
        """
            Test api get Role Title Detail response code 000
            Step by step:
            - Tạo company, department trên DB
            - Tạo role title gắn với company gắn với department trên DB
            - Gọi API Role Title Detail với đầu vào chuẩn
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . department_id đúng department
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id})
        role_title = fake.role_title_provider(
            {'company_id': company.id, 'department_id': department.id, 'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/role_titles/{role_title.id}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['id'] == role_title.id
        assert data.get('data')['department_id'] == department.id

    def test_191_response_role_title_not_exits(self, client: TestClient):
        """
            Test api get Role Title Detail response code 191
            Step by step:
            - Tạo company, department trên DB
            - Tạo role title gắn với company gắn với department trên DB
            - Gọi API Role Title Detail với role_title_id không tồn tại trong hệ thống
            - Đầu ra mong muốn:
                . status code: 400
                . code: 191
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id})
        role_title = fake.role_title_provider(
            {'company_id': company.id, 'department_id': department.id, 'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/role_titles/{role_title.id + 1}")
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '191'
        assert data.get('message') == 'role title id không tồn tại'

    def test_999_internal_error(self, client: TestClient):
        """
            Test api get Role Title Detail response code 999
            Step by step:
            - Gọi API Role Title Detail lỗi
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
