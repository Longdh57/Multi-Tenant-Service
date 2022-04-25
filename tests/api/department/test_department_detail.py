import json
import random

from fastapi.encoders import jsonable_encoder
from fastapi_sqlalchemy import db
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from app.core.config import settings
from app.models import DepartmentStaff
from app.schemas.sche_base import ResponseSchemaBase
from tests.api import APITestCase
from tests.faker import fake


class TestGetDepartmentDetailAPI(APITestCase):
    ISSUE_KEY = "O2OSTAFF-284"

    def test_000_response(self, client: TestClient):
        """
            Test api get Department Detail response code 000
            Step by step:
            - Tạo 1 Department trong DB
            - Gọi API Department Detail với đầu vào chuẩn
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id})
        resp = client.get(f"{settings.BASE_API_PREFIX}/departments/{department.id}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['department_name'] == department.department_name
        assert data.get('data')['company']['id'] == company.id

    def test_000_response_normal_with_zero_staff(self, client: TestClient):
        """
            Test api get Department Detail response code 000
            Step by step:
            - Tạo 1 Department trong DB
            - Gọi API Department Detail với đầu vào chuẩn & không có staff kèm theo
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id})
        resp = client.get(f"{settings.BASE_API_PREFIX}/departments/{department.id}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['department_name'] == department.department_name
        assert data.get('data')['company']['id'] == company.id
        assert len(data.get('data')['staff']) == 0

    def test_000_response_none_parent(self, client: TestClient):
        """
            Test api get Department Detail response code 000
            Step by step:
            - Tạo 1 Department trong DB
            - Gọi API Department Detail với đầu vào chuẩn & không có department cha
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id})
        resp = client.get(f"{settings.BASE_API_PREFIX}/departments/{department.id}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['department_name'] == department.department_name
        assert data.get('data')['company']['id'] == company.id
        assert data.get('data')['parent'] == None

    def test_000_response_with_department_have_parent_id(self, client: TestClient):
        """
            Test api get Department Detail response code 000
            Step by step:
            - Tạo 1 Department cha trong DB
            - Tạo 1 Department con trong DB
            - Gọi API Department Detail với đầu vào là id của department con
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        department_parent = fake.department({'company_id': company.id})
        department = fake.department({
            'company_id': company.id,
            'parent_id': department_parent.id
        })

        resp = client.get(f"{settings.BASE_API_PREFIX}/departments/{department.id}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['department_name'] == department.department_name
        assert data.get('data')['company']['id'] == company.id
        assert data.get('data')['parent']['id'] == department_parent.id

    def test_000_response_with_department_have_3_children(self, client: TestClient):
        """
            Test api get Department Detail response code 000
            Step by step:
            - Tạo 1 Department cha trong DB
            - Tạo 3 Department con trong DB
            - Gọi API Department Detail với đầu vào là id của department cha
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . detail có đúng 3 children con
        """
        company = fake.company_provider()
        department_parent = fake.department({'company_id': company.id})
        for _ in range(3):
            fake.department({'company_id': company.id, 'parent_id': department_parent.id})

        resp = client.get(f"{settings.BASE_API_PREFIX}/departments/{department_parent.id}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['department_name'] == department_parent.department_name
        assert data.get('data')['company']['id'] == company.id
        assert len(data.get('data')['children']) == 3

    def test_000_response_with_3_level_department(self, client: TestClient):
        """
            Test api get Department Detail response code 000
            Step by step:
            - Tạo 1 Department cha trong DB
            - Tạo 1 Department con trong DB
            - Tạo 1 Department con tiep theo trong DB
            - Gọi API Department Detail với đầu vào là id của Department con (department ở giữa)
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . detail có 1 children con
                . detail có 1 parent
        """
        company = fake.company_provider()
        department_parent = fake.department({'company_id': company.id})
        department = fake.department({'company_id': company.id, 'parent_id': department_parent.id})
        department_child = fake.department({'company_id': company.id, 'parent_id': department.id})

        resp = client.get(f"{settings.BASE_API_PREFIX}/departments/{department.id}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['department_name'] == department.department_name
        assert data.get('data')['company']['id'] == company.id
        assert len(data.get('data')['children']) == 1
        assert data.get('data')['children'][0]['department']['id'] == department_child.id
        assert data.get('data')['parent']['id'] == department_parent.id

    def test_000_response_multi_staff(self, client: TestClient):
        """
            Test api get Department Detail response code 000
            Step by step:
            - Tạo 1 company, 1 Department, 1 list staff, 1 list role_title trong DB
            - Thêm Staff vào department
            - Gọi API Department Detail
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . detail có số lượng staff bằng số staff đã thêm vào department
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id})
        number_staffs = random.randint(2, 10)
        staffs = [fake.staff_provider({'company_id': company.id, 'is_active': True}) for _ in range(number_staffs)]
        role_titles = [fake.role_title_provider({
            'company_id': company.id, 'department_id': department.id, 'is_active': True}) for _ in range(number_staffs)]

        department_staff_mappings = [{
            'department_id': department.id,
            'staff_id': staff.id,
            'role_title_id': random.choice(role_titles).id,
            'is_active': True
        } for staff in staffs]
        with db():
            db.session.bulk_insert_mappings(DepartmentStaff, department_staff_mappings)
            db.session.commit()

        resp = client.get(f"{settings.BASE_API_PREFIX}/departments/{department.id}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['department_name'] == department.department_name
        assert data.get('data')['company']['id'] == company.id
        assert len(data.get('data')['staff']) == number_staffs

    def test_091_response_department_not_exits(self, client: TestClient):
        """
            Test api get Department Detail response code 091
            Step by step:
            - Tạo 1 Department trong DB
            - Gọi API Department Detail với department_id không tồn tại trong hệ thống
            - Đầu ra mong muốn:
                . status code: 400
                . code: 091
        """
        department = fake.department()
        resp = client.get(f"{settings.BASE_API_PREFIX}/departments/10000000")
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '091'
        assert data.get('message') == 'ID của phòng ban không tồn tại trong hệ thống'

    def test_999_internal_error(self, client: TestClient):
        """
            Test api get Department Detail response code 999
            Step by step:
            - Gọi API Department Detail lỗi
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
