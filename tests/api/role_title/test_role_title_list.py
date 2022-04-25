import json
import random

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from app.core.config import settings
from app.schemas.sche_base import ResponseSchemaBase
from tests.api import APITestCase
from tests.faker import fake


class TestGetRoleTitleListAPI(APITestCase):
    ISSUE_KEY = "O2OSTAFF-288"

    def test_000_response_normal(self, client: TestClient):
        """
            Test api get Role Title List response code 000
            Step by step:
            - Tạo n Role Title trên DB
            - Gọi API Role Title List với đầu vào chuẩn
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . Số lượng role title bằng số đã tạo trong DB
        """
        company = fake.company_provider()
        total_role_titles = random.randint(2, 100)
        fake.role_titles(company=company, total=total_role_titles)

        resp = client.get(f"{settings.BASE_API_PREFIX}/role_titles?company_id={company.id}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert len(data.get('data')) == total_role_titles

    def test_000_response_all_is_active_status(self, client: TestClient):
        """
            Test api get Role Title List response code 000
            Step by step:
            - Tạo 10 Role Title trên DB, trong đó có 6 role_title active, 4 inactive
            - Gọi API Role Title List với đầu vào chuẩn
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . Số lượng role title bằng 10
        """
        company = fake.company_provider()
        for i in range(10):
            fake.role_title_provider({'company_id': company.id, 'is_active': (i < 6)})

        resp = client.get(f"{settings.BASE_API_PREFIX}/role_titles?company_id={company.id}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert len(data.get('data')) == 10

    def test_000_response_with_department_id(self, client: TestClient):
        """
            Test api get Role Title List response code 000
            Step by step:
            - Tạo department trên DB
            - Tạo n Role Title trên DB gắn với department
            - Gọi API Role Title List với params gồm department_id
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . Số lượng role title bằng số đã tạo trong DB
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id})
        total_role_titles = random.randint(2, 10)
        for _ in range(total_role_titles):
            fake.role_title_provider({'company_id': company.id, 'department_id': department.id})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/role_titles?company_id={company.id}&department_id={department.id}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert len(data.get('data')) == total_role_titles

    def test_000_response_with_department_id_not_exists(self, client: TestClient):
        """
            Test api get Role Title List response code 000
            Step by step:
            - Tạo department trên DB
            - Tạo n Role Title trên DB gắn với department
            - Gọi API Role Title List với params gồm department_id không tồn tại
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . Số lượng role title bằng 0
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id})
        total_role_titles = random.randint(2, 10)
        for _ in range(total_role_titles):
            fake.role_title_provider({'company_id': company.id, 'department_id': department.id})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/role_titles?company_id={company.id}&department_id={department.id + 1}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert len(data.get('data')) == 0

    def test_000_response_with_role_title_name_search_like(self, client: TestClient):
        """
            Test api get Role Title List response code 000
            Step by step:
            - Tạo company trên DB
            - Tạo 2 Role Title trên DB gắn với company có tên "Chức vụ số 1", "Test chức vụ %&*^"
            - Gọi API Role Title List với params gồm role_title_name = 'chức'
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . Số lượng role title bằng 2
        """
        company = fake.company_provider()
        fake.role_title_provider({'company_id': company.id, 'role_title_name': 'Chức vụ số 1', 'is_active': True})
        fake.role_title_provider({'company_id': company.id, 'role_title_name': 'Test chức vụ %&*^', 'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/role_titles?company_id={company.id}&role_title_name=chức")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert len(data.get('data')) == 2

    def test_000_response_with_role_title_name_search_exactly(self, client: TestClient):
        """
            Test api get Role Title List response code 000
            Step by step:
            - Tạo company trên DB
            - Tạo 2 Role Title trên DB gắn với company có tên "Chức vụ số 1", "Test chức vụ %&*^"
            - Gọi API Role Title List với params gồm role_title_name = 'Chức vụ số 1'
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . Số lượng role title bằng 2
        """
        company = fake.company_provider()
        fake.role_title_provider({'company_id': company.id, 'role_title_name': 'Chức vụ số 1', 'is_active': True})
        fake.role_title_provider({'company_id': company.id, 'role_title_name': 'Test chức vụ %&*^', 'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/role_titles?company_id={company.id}&role_title_name={'Chức vụ số 1'}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert len(data.get('data')) == 1

    def test_000_response_with_role_title_name_not_exists(self, client: TestClient):
        """
            Test api get Role Title List response code 000
            Step by step:
            - Tạo company trên DB
            - Tạo 2 Role Title trên DB gắn với company có tên "Chức vụ số 1", "Test chức vụ %&*^"
            - Gọi API Role Title List với params gồm role_title_name = 'aaaa'
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . Số lượng role title bằng 0
        """
        company = fake.company_provider()
        fake.role_title_provider({'company_id': company.id, 'role_title_name': 'Chức vụ số 1', 'is_active': True})
        fake.role_title_provider({'company_id': company.id, 'role_title_name': 'Test chức vụ %&*^', 'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/role_titles?company_id={company.id}&role_title_name=aaaa")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert len(data.get('data')) == 0

    def test_000_response_with_role_title_name_capitalization(self, client: TestClient):
        """
            Test api get Role Title List response code 000
            Step by step:
            - Tạo company trên DB
            - Tạo 2 Role Title trên DB gắn với company có tên "Chức vụ số 1", "Test chức vụ %&*^"
            - Gọi API Role Title List với params gồm role_title_name = 'CHỨC'
            - Gọi API Role Title List với params gồm role_title_name = 'chức'
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . Trong cả 2 TH số lượng role title bằng 2
        """
        company = fake.company_provider()
        fake.role_title_provider({'company_id': company.id, 'role_title_name': 'Chức vụ số 1', 'is_active': True})
        fake.role_title_provider({'company_id': company.id, 'role_title_name': 'Test chức vụ %&*^', 'is_active': True})

        for search_value in ['CHỨC', 'chức']:
            resp = client.get(
                f"{settings.BASE_API_PREFIX}/role_titles?company_id={company.id}&role_title_name={search_value}")
            data = resp.json()

            assert resp.status_code == 200
            assert data.get('code') == '000'
            assert data.get('message') == 'Thành công'
            assert len(data.get('data')) == 2

    def test_000_response_with_role_title_name_and_department_id(self, client: TestClient):
        """
            Test api get Role Title List response code 000
            Step by step:
            - Tạo company, department1, department2 trên DB
            - Tạo Role Title 1 trên DB gắn với department1 có tên "Chức vụ số 1"
            - Tạo Role Title 2 trên DB gắn với department2 có tên "Chức vụ số 1"
            - Gọi API Role Title List với params gồm role_title_name = 'chức' & department_id = department1
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . Số lượng role title bằng 1
        """
        company = fake.company_provider()
        department1 = fake.department({'company_id': company.id})
        department2 = fake.department({'company_id': company.id})
        fake.role_title_provider(
            {'company_id': company.id, 'department_id': department1.id, 'role_title_name': 'Chức vụ số 1',
             'is_active': True})
        fake.role_title_provider(
            {'company_id': company.id, 'department_id': department2.id, 'role_title_name': 'Chức vụ số 1',
             'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/role_titles?company_id={company.id}&role_title_name=chức&department_id={department1.id}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert len(data.get('data')) == 1

    def test_092_response_company_id_not_null(self, client: TestClient):
        """
            Test api get Role Title List response code 092
            Step by step:
            - Tạo n Role Title trên DB
            - Gọi API Role Title List với param: không có company_id
            - Đầu ra mong muốn:
                . status code: 400
                . code: 092
        """
        company = fake.company_provider()
        fake.role_titles(company=company, total=random.randint(2, 100))
        resp = client.get(
            f"{settings.BASE_API_PREFIX}/role_titles")
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '092'
        assert data.get('message') == 'ID của company không được để trống'

    def test_999_internal_error(self, client: TestClient):
        """
            Test api get Role Title List response code 999
            Step by step:
            - Gọi API Role Title List lỗi
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
