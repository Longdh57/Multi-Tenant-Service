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


class TestPostDepartmentAddStaffAPI(APITestCase):
    ISSUE_KEY = "O2OSTAFF-286"

    def test_000_response(self, client: TestClient):
        """
            Test api get Department Detail response code 000
            Step by step:
            - Tạo 1 Department, role_title gắn với department trong DB
            - Tạo n Staff trong DB
            - Gọi API Department Add Staff với đầu vào list staff
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id, 'is_active': True})
        role_title = fake.role_title_provider(
            {'company_id': company.id, 'department_id': department.id, 'is_active': True})
        total_staffs = random.randint(2, 10)
        staffs = [fake.staff_provider({'company_id': company.id, 'is_active': True}) for _ in
                  range(total_staffs)]

        add_staff_body = {
            'department_id': department.id,
            'staffs': [{
                'staff_id': staff.id,
                'role_title_id': role_title.id,
            } for staff in staffs]
        }

        resp = client.post(f"{settings.BASE_API_PREFIX}/departments/staff/add", json=jsonable_encoder(add_staff_body))
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        with db():
            assert db.session.query(DepartmentStaff).filter(
                DepartmentStaff.department_id == department.id,
                DepartmentStaff.staff_id.in_([staff.id for staff in staffs]),
                DepartmentStaff.is_active == True
            ).count() == total_staffs

    def test_091_response_department_not_exists(self, client: TestClient):
        """
            Test api get Department Detail response code 091
            Step by step:
            - Tạo 1 Department, role_title gắn với department trong DB
            - Tạo n Staff trong DB
            - Gọi API Department Add Staff với đầu vào list staff và department ko tồn tại
            - Đầu ra mong muốn:
                . status code: 400
                . code: 091
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id, 'is_active': True})
        role_title = fake.role_title_provider(
            {'company_id': company.id, 'department_id': department.id, 'is_active': True})
        total_staffs = random.randint(2, 10)
        staffs = [fake.staff_provider({'company_id': company.id, 'is_active': True}) for _ in
                  range(total_staffs)]

        add_staff_body = {
            'department_id': department.id + 1,
            'staffs': [{
                'staff_id': staff.id,
                'role_title_id': role_title.id,
            } for staff in staffs]
        }

        resp = client.post(f"{settings.BASE_API_PREFIX}/departments/staff/add", json=jsonable_encoder(add_staff_body))
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '091'
        assert data.get('message') == 'ID của phòng ban không tồn tại trong hệ thống'

    def test_097_response_staff_and_department_not_same_company(self, client: TestClient):
        """
            Test api get Department Detail response code 097
            Step by step:
            - Tạo company1, company2 trong DB
            - Tạo 1 Department, role_title gắn với company1 trong DB
            - Tạo n Staff nhưng gắn với company2 trong DB
            - Gọi API Department Add Staff với đầu vào staff và department
            - Đầu ra mong muốn:
                . status code: 400
                . code: 097
        """
        company1 = fake.company_provider()
        company2 = fake.company_provider()
        department = fake.department({'company_id': company1.id, 'is_active': True})
        role_title = fake.role_title_provider(
            {'company_id': company1.id, 'department_id': department.id, 'is_active': True})
        total_staffs = random.randint(2, 10)
        staffs = [fake.staff_provider({'company_id': company2.id, 'is_active': True}) for _ in
                  range(total_staffs)]

        add_staff_body = {
            'department_id': department.id,
            'staffs': [{
                'staff_id': staff.id,
                'role_title_id': role_title.id,
            } for staff in staffs]
        }

        resp = client.post(f"{settings.BASE_API_PREFIX}/departments/staff/add", json=jsonable_encoder(add_staff_body))
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '097'
        assert data.get('message') == 'Nhân viên và phòng ban không thuộc cùng công ty'

    def test_098_response_role_title_not_belong_to_department(self, client: TestClient):
        """
            Test api get Department Detail response code 098
            Step by step:
            - Tạo company trong DB
            - Tạo department1, n Staff trong DB
            - Tạo department2, role_title gắn với department2 trong DB
            - Gọi API Department Add Staff với đầu vào staff, department1 và role_title của department2
            - Đầu ra mong muốn:
                . status code: 400
                . code: 098
        """
        company = fake.company_provider()
        department1 = fake.department({'company_id': company.id, 'is_active': True})
        department2 = fake.department({'company_id': company.id, 'is_active': True})
        role_title = fake.role_title_provider(
            {'company_id': company.id, 'department_id': department2.id, 'is_active': True})
        total_staffs = random.randint(2, 10)
        staffs = [fake.staff_provider({'company_id': company.id, 'is_active': True}) for _ in
                  range(total_staffs)]

        add_staff_body = {
            'department_id': department1.id,
            'staffs': [{
                'staff_id': staff.id,
                'role_title_id': role_title.id,
            } for staff in staffs]
        }

        resp = client.post(f"{settings.BASE_API_PREFIX}/departments/staff/add", json=jsonable_encoder(add_staff_body))
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '098'
        assert data.get('message') == 'Role_title không thuộc phòng ban'

    def test_101_response_role_title_inactive(self, client: TestClient):
        """
            Test api get Department Detail response code 101
            Step by step:
            - Tạo company trong DB
            - Tạo department, n Staff trong DB
            - Tạo role_title gắn với department trong DB nhưng is_active = False
            - Gọi API Department Add Staff với đầu vào staff, department và role_title
            - Đầu ra mong muốn:
                . status code: 400
                . code: 101
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id, 'is_active': True})
        role_title = fake.role_title_provider(
            {'company_id': company.id, 'department_id': department.id, 'is_active': False})
        total_staffs = random.randint(2, 10)
        staffs = [fake.staff_provider({'company_id': company.id, 'is_active': True}) for _ in
                  range(total_staffs)]

        add_staff_body = {
            'department_id': department.id,
            'staffs': [{
                'staff_id': staff.id,
                'role_title_id': role_title.id,
            } for staff in staffs]
        }

        resp = client.post(f"{settings.BASE_API_PREFIX}/departments/staff/add", json=jsonable_encoder(add_staff_body))
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '101'
        assert data.get('message') == 'Role_title đã khóa'

    def test_102_response_staff_id_duplicate(self, client: TestClient):
        """
            Test api get Department Detail response code 102
            Step by step:
            - Tạo company trong DB
            - Tạo department, role_title, n Staff trong DB
            - Gọi API Department Add Staff với đầu vào staff, department và role_title nhưng staff bị trùng
            - Đầu ra mong muốn:
                . status code: 400
                . code: 102
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id, 'is_active': True})
        role_title = fake.role_title_provider(
            {'company_id': company.id, 'department_id': department.id, 'is_active': False})
        total_staffs = random.randint(2, 10)
        staffs = [fake.staff_provider({'company_id': company.id, 'is_active': True}) for _ in
                  range(total_staffs)]

        add_staff_body = {
            'department_id': department.id,
            'staffs': [{
                'staff_id': staffs[0].id,
                'role_title_id': role_title.id,
            } for _ in staffs]
        }

        resp = client.post(f"{settings.BASE_API_PREFIX}/departments/staff/add", json=jsonable_encoder(add_staff_body))
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '102'
        assert data.get('message') == 'Staff_id bị duplicate'

    def test_105_response_staff_id_belong_to_other_department(self, client: TestClient):
        """
            Test api get Department Detail response code 105
            Step by step:
            - Tạo company trong DB
            - Tạo department1, role_title tương ứng và 1 Staff trong DB
            - Gán staff vào department1 ở trạng thái active
            - Tạo department2, role_title tương ứng
            - Gọi API Department Add Staff với đầu vào staff, department2 và role_title2 (staff đã thuộc department1)
            - Đầu ra mong muốn:
                . status code: 400
                . code: 105
        """
        company = fake.company_provider()
        department1 = fake.department({'company_id': company.id, 'is_active': True})
        role_title1 = fake.role_title_provider(
            {'company_id': company.id, 'department_id': department1.id, 'is_active': False})
        staff = fake.staff_provider({'company_id': company.id, 'is_active': True})
        department_staff_mappings = [{
            'department_id': department1.id,
            'staff_id': staff.id,
            'role_title_id': role_title1.id,
            'is_active': True
        }]
        with db():
            db.session.bulk_insert_mappings(DepartmentStaff, department_staff_mappings)
            db.session.commit()

        department2 = fake.department({'company_id': company.id, 'is_active': True})
        role_title2 = fake.role_title_provider(
            {'company_id': company.id, 'department_id': department2.id, 'is_active': False})

        add_staff_body = {
            'department_id': department2.id,
            'staffs': [{
                'staff_id': staff.id,
                'role_title_id': role_title2.id,
            }]
        }

        resp = client.post(f"{settings.BASE_API_PREFIX}/departments/staff/add", json=jsonable_encoder(add_staff_body))
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '105'
        assert 'Staff đã thuộc department khác' in data.get('message')

    def test_106_response_staff_inactive(self, client: TestClient):
        """
            Test api get Department Detail response code 106
            Step by step:
            - Tạo 1 Department, role_title gắn với department trong DB
            - Tạo n Staff is_active=False trong DB
            - Gọi API Department Add Staff với đầu vào list staff
            - Đầu ra mong muốn:
                . status code: 400
                . code: 106
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id, 'is_active': True})
        role_title = fake.role_title_provider(
            {'company_id': company.id, 'department_id': department.id, 'is_active': True})
        total_staffs = random.randint(2, 10)
        staffs = [fake.staff_provider({'company_id': company.id, 'is_active': False}) for _ in
                  range(total_staffs)]

        add_staff_body = {
            'department_id': department.id,
            'staffs': [{
                'staff_id': staff.id,
                'role_title_id': role_title.id,
            } for staff in staffs]
        }

        resp = client.post(f"{settings.BASE_API_PREFIX}/departments/staff/add", json=jsonable_encoder(add_staff_body))
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '106'
        assert 'Staff đã bị inactive' in data.get('message')

    def test_107_response_department_inactive(self, client: TestClient):
        """
            Test api get Department Detail response code 107
            Step by step:
            - Tạo 1 Department is_active=False, role_title gắn với department trong DB
            - Tạo n Staff trong DB
            - Gọi API Department Add Staff với đầu vào list staff
            - Đầu ra mong muốn:
                . status code: 400
                . code: 107
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id, 'is_active': False})
        role_title = fake.role_title_provider(
            {'company_id': company.id, 'department_id': department.id, 'is_active': True})
        total_staffs = random.randint(2, 10)
        staffs = [fake.staff_provider({'company_id': company.id, 'is_active': True}) for _ in
                  range(total_staffs)]

        add_staff_body = {
            'department_id': department.id,
            'staffs': [{
                'staff_id': staff.id,
                'role_title_id': role_title.id,
            } for staff in staffs]
        }

        resp = client.post(f"{settings.BASE_API_PREFIX}/departments/staff/add", json=jsonable_encoder(add_staff_body))
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '107'
        assert data.get('message') == 'Phòng ban đã bị inactive'

    def test_134_response_staff_id_not_exists(self, client: TestClient):
        """
            Test api get Department Detail response code 134
            Step by step:
            - Tạo company trong DB
            - Tạo department, role_title, n Staff trong DB
            - Gọi API Department Add Staff với đầu vào staff không tồn tại, department và role_title đã có sẵn
            - Đầu ra mong muốn:
                . status code: 400
                . code: 134
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id, 'is_active': True})
        role_title = fake.role_title_provider(
            {'company_id': company.id, 'department_id': department.id, 'is_active': False})
        total_staffs = random.randint(2, 10)
        staffs = [fake.staff_provider({'company_id': company.id, 'is_active': True}) for _ in
                  range(total_staffs)]

        add_staff_body = {
            'department_id': department.id,
            'staffs': [{
                'staff_id': staff.id + 1000,
                'role_title_id': role_title.id,
            } for staff in staffs]
        }

        resp = client.post(f"{settings.BASE_API_PREFIX}/departments/staff/add", json=jsonable_encoder(add_staff_body))
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '134'
        assert data.get('message') == 'Id của staff không tồn tại'

    def test_191_response_role_title_id_not_exists(self, client: TestClient):
        """
            Test api get Department Detail response code 191
            Step by step:
            - Tạo company trong DB
            - Tạo department, n Staff trong DB
            - Gọi API Department Add Staff với đầu vào staff, department nhưng role_title không tồn tại
            - Đầu ra mong muốn:
                . status code: 400
                . code: 191
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id, 'is_active': True})
        total_staffs = random.randint(2, 10)
        staffs = [fake.staff_provider({'company_id': company.id, 'is_active': True}) for _ in
                  range(total_staffs)]

        add_staff_body = {
            'department_id': department.id,
            'staffs': [{
                'staff_id': staff.id,
                'role_title_id': 1,
            } for staff in staffs]
        }

        resp = client.post(f"{settings.BASE_API_PREFIX}/departments/staff/add", json=jsonable_encoder(add_staff_body))
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '191'
        assert data.get('message') == 'role title id không tồn tại'

    def test_990_server_maintain(self, client: TestClient):
        """
            Test api POST Create/Update Department response code 990
            Step by step:
            - Gọi POST Create/Update Department lỗi
            - Đầu ra mong muốn:
                . status code: 500
                . code: 990
        """
        res = JSONResponse(
            status_code=500,
            content=jsonable_encoder(
                ResponseSchemaBase().custom_response(
                    '990', "Hệ thống đang bảo trì, quý khách vui lòng thử lại sau"
                )
            )
        )
        assert res.status_code == 500 and json.loads(res.body) == {
            "code": "990",
            "message": "Hệ thống đang bảo trì, quý khách vui lòng thử lại sau"
        }

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
