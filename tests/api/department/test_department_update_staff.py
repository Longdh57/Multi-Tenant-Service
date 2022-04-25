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


class TestPutDepartmentUpdateStaffAPI(APITestCase):
    ISSUE_KEY = "O2OSTAFF-287"

    def test_000_response_update_is_active_equal_false(self, client: TestClient):
        """
            Test api PUT update Department Staff response code 000
            Step by step:
            - Tạo company, department, role_title, staff
            - Gán department-staff với is_active = True
            - Gọi API Department Update Staff update is_active = False
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id, 'is_active': True})
        role_title = fake.role_title_provider({
            'company_id': company.id, 'department_id': department.id, 'is_active': True})
        staff = fake.staff_provider({'company_id': company.id, 'is_active': True})
        department_staff = DepartmentStaff(
            department_id=department.id,
            staff_id=staff.id,
            role_title_id=role_title.id,
            is_active=True
        )
        with db():
            db.session.add(department_staff)
            db.session.commit()

        update_dept_staff = {
            "department_id": department.id,
            "staff_id": staff.id,
            "role_title_id": role_title.id,
            "is_active": False
        }
        resp = client.put(f"{settings.BASE_API_PREFIX}/departments/staff/update",
                          json=jsonable_encoder(update_dept_staff))
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'

    def test_000_response_update_role_title_and_is_active(self, client: TestClient):
        """
            Test api PUT update Department Staff response code 000
            Step by step:
            - Tạo company, department, role_title1, role_title2, staff
            - Gán department-staff với is_active = True & role_title1
            - Gọi API Department Update Staff update role_title2
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id, 'is_active': True})
        role_title1 = fake.role_title_provider({
            'company_id': company.id, 'department_id': department.id, 'is_active': True})
        role_title2 = fake.role_title_provider({
            'company_id': company.id, 'department_id': department.id, 'is_active': True})
        staff = fake.staff_provider({'company_id': company.id, 'is_active': True})
        department_staff = DepartmentStaff(
            department_id=department.id,
            staff_id=staff.id,
            role_title_id=role_title1.id,
            is_active=True
        )
        with db():
            db.session.add(department_staff)
            db.session.commit()

        update_dept_staff = {
            "department_id": department.id,
            "staff_id": staff.id,
            "role_title_id": role_title2.id,
            "is_active": False
        }
        resp = client.put(f"{settings.BASE_API_PREFIX}/departments/staff/update",
                          json=jsonable_encoder(update_dept_staff))
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'

    def test_000_response_create_department_staff(self, client: TestClient):
        """
            Test api PUT update Department Staff response code 000
            Step by step:
            - Tạo company, department, role_title, staff
            - Gọi API Department Update Staff create department-staff
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id, 'is_active': True})
        role_title = fake.role_title_provider({
            'company_id': company.id, 'department_id': department.id, 'is_active': True})
        staff = fake.staff_provider({'company_id': company.id, 'is_active': True})

        update_dept_staff = {
            "department_id": department.id,
            "staff_id": staff.id,
            "role_title_id": role_title.id,
            "is_active": True
        }
        resp = client.put(f"{settings.BASE_API_PREFIX}/departments/staff/update",
                          json=jsonable_encoder(update_dept_staff))
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        with db():
            assert db.session.query(DepartmentStaff).filter(
                DepartmentStaff.department_id == department.id,
                DepartmentStaff.staff_id == staff.id,
                DepartmentStaff.role_title_id == role_title.id,
                DepartmentStaff.is_active == True
            ).count() == 1

    def test_000_response_update_a_department_staff_being_inactive_to_other_role_title(self, client: TestClient):
        """
            Test api PUT update Department Staff response code 000
            Step by step:
            - Tạo company, department, role_title1, role_title2, staff
            - Gán department-staff với is_active = True & role_title1
            - Gọi API Department Update Staff update role_title2
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id, 'is_active': True})
        role_title1 = fake.role_title_provider({
            'company_id': company.id, 'department_id': department.id, 'is_active': True})
        role_title2 = fake.role_title_provider({
            'company_id': company.id, 'department_id': department.id, 'is_active': True})
        staff = fake.staff_provider({'company_id': company.id, 'is_active': True})
        department_staff = DepartmentStaff(
            department_id=department.id,
            staff_id=staff.id,
            role_title_id=role_title1.id,
            is_active=False
        )
        with db():
            db.session.add(department_staff)
            db.session.commit()

        update_dept_staff = {
            "department_id": department.id,
            "staff_id": staff.id,
            "role_title_id": role_title2.id,
            "is_active": True
        }
        resp = client.put(f"{settings.BASE_API_PREFIX}/departments/staff/update",
                          json=jsonable_encoder(update_dept_staff))
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'

    def test_000_response_create_department_staff_with_all_other_department_staff_inactive(self, client: TestClient):
        """
            Test api PUT update Department Staff response code 000
            Step by step:
            - Tạo company, department1, role_title1, staff
            - Gán department-staff với is_active = False & department1, role_title1
            - Tạo company, department2, role_title2
            - Gọi API Department Update Staff create với department2, role_title2, staff
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . tạo mới một department-staff
        """
        company = fake.company_provider()
        department1 = fake.department({'company_id': company.id, 'is_active': True})
        role_title1 = fake.role_title_provider({
            'company_id': company.id, 'department_id': department1.id, 'is_active': True})
        staff = fake.staff_provider({'company_id': company.id, 'is_active': True})
        department_staff = DepartmentStaff(
            department_id=department1.id,
            staff_id=staff.id,
            role_title_id=role_title1.id,
            is_active=False
        )
        with db():
            db.session.add(department_staff)
            db.session.commit()
        department2 = fake.department({'company_id': company.id, 'is_active': True})
        role_title2 = fake.role_title_provider({
            'company_id': company.id, 'department_id': department2.id, 'is_active': True})

        update_dept_staff = {
            "department_id": department2.id,
            "staff_id": staff.id,
            "role_title_id": role_title2.id,
            "is_active": True
        }
        resp = client.put(f"{settings.BASE_API_PREFIX}/departments/staff/update",
                          json=jsonable_encoder(update_dept_staff))
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        with db():
            assert db.session.query(DepartmentStaff).filter(
                DepartmentStaff.department_id == department2.id,
                DepartmentStaff.staff_id == staff.id,
                DepartmentStaff.role_title_id == role_title2.id,
                DepartmentStaff.is_active == True
            ).count() == 1

    def test_091_response_update_department_id_not_exists(self, client: TestClient):
        """
            Test api PUT update Department Staff response code 091
            Step by step:
            - Tạo company, department, role_title, staff
            - Gán department-staff với is_active = True & role_title
            - Gọi API Department Update Staff update department_id không tồn tại
            - Đầu ra mong muốn:
                . status code: 400
                . code: 091
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id, 'is_active': True})
        role_title = fake.role_title_provider({
            'company_id': company.id, 'department_id': department.id, 'is_active': True})
        staff = fake.staff_provider({'company_id': company.id, 'is_active': True})
        department_staff = DepartmentStaff(
            department_id=department.id,
            staff_id=staff.id,
            role_title_id=role_title.id,
            is_active=True
        )
        with db():
            db.session.add(department_staff)
            db.session.commit()

        update_dept_staff = {
            "department_id": department.id + 1,
            "staff_id": staff.id,
            "role_title_id": role_title.id,
            "is_active": True
        }
        resp = client.put(f"{settings.BASE_API_PREFIX}/departments/staff/update",
                          json=jsonable_encoder(update_dept_staff))
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '091'
        assert data.get('message') == 'ID của phòng ban không tồn tại trong hệ thống'

    def test_097_response_create_staff_department_not_same_company(self, client: TestClient):
        """
            Test api PUT update Department Staff response code 097
            Step by step:
            - Tạo company1,company2 trong DB
            - Tạo department, role_title gắn với company1
            - Tạo staff gắn với company2
            - Gọi API Department Update Staff để create với department_id và staff_id thuộc 2 cty
            - Đầu ra mong muốn:
                . status code: 400
                . code: 097
        """
        company1 = fake.company_provider()
        company2 = fake.company_provider()
        department = fake.department({'company_id': company1.id, 'is_active': True})
        role_title = fake.role_title_provider({
            'company_id': company1.id, 'department_id': department.id, 'is_active': True})
        staff = fake.staff_provider({'company_id': company2.id, 'is_active': True})

        update_dept_staff = {
            "department_id": department.id,
            "staff_id": staff.id,
            "role_title_id": role_title.id,
            "is_active": True
        }
        resp = client.put(f"{settings.BASE_API_PREFIX}/departments/staff/update",
                          json=jsonable_encoder(update_dept_staff))
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '097'
        assert data.get('message') == 'Nhân viên và phòng ban không thuộc cùng công ty'

    def test_098_response_create_staff_department_with_role_not_belong_to_department(self, client: TestClient):
        """
            Test api PUT update Department Staff response code 098
            Step by step:
            - Tạo company, staff trong DB
            - Tạo department1, role_title1
            - Tạo department2, role_title2
            - Gọi API Department Update Staff để create với department1, role_title2 và staff_id
            - Đầu ra mong muốn:
                . status code: 400
                . code: 098
        """
        company = fake.company_provider()
        department1 = fake.department({'company_id': company.id, 'is_active': True})
        role_title1 = fake.role_title_provider({
            'company_id': company.id, 'department_id': department1.id, 'is_active': True})
        department2 = fake.department({'company_id': company.id, 'is_active': True})
        role_title2 = fake.role_title_provider({
            'company_id': company.id, 'department_id': department2.id, 'is_active': True})
        staff = fake.staff_provider({'company_id': company.id, 'is_active': True})

        update_dept_staff = {
            "department_id": department1.id,
            "staff_id": staff.id,
            "role_title_id": role_title2.id,
            "is_active": True
        }
        resp = client.put(f"{settings.BASE_API_PREFIX}/departments/staff/update",
                          json=jsonable_encoder(update_dept_staff))
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '098'
        assert data.get('message') == 'Role_title không thuộc phòng ban'

    def test_098_response_update_staff_department_with_role_not_belong_to_department(self, client: TestClient):
        """
            Test api PUT update Department Staff response code 098
            Step by step:
            - Tạo company, staff trong DB
            - Tạo department1, role_title1, department-staff
            - Tạo department2, role_title2
            - Gọi API Department Update Staff để update với department1, role_title2 và staff_id
            - Đầu ra mong muốn:
                . status code: 400
                . code: 098
        """
        company = fake.company_provider()
        department1 = fake.department({'company_id': company.id, 'is_active': True})
        role_title1 = fake.role_title_provider({
            'company_id': company.id, 'department_id': department1.id, 'is_active': True})
        department2 = fake.department({'company_id': company.id, 'is_active': True})
        role_title2 = fake.role_title_provider({
            'company_id': company.id, 'department_id': department2.id, 'is_active': True})
        staff = fake.staff_provider({'company_id': company.id, 'is_active': True})

        update_dept_staff = {
            "department_id": department1.id,
            "staff_id": staff.id,
            "role_title_id": role_title2.id,
            "is_active": True
        }
        resp = client.put(f"{settings.BASE_API_PREFIX}/departments/staff/update",
                          json=jsonable_encoder(update_dept_staff))
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '098'
        assert data.get('message') == 'Role_title không thuộc phòng ban'

    def test_105_response_update_staff_belong_to_other_department(self, client: TestClient):
        """
            Test api PUT update Department Staff response code 105
            Step by step:
            - Tạo company, department1, role_title1, staff
            - Gán department1-staff với is_active = True
            - Tạo department2, role_title2
            - Gọi API Department Update Staff update với department2, role_title2, staff
            - Đầu ra mong muốn:
                . status code: 400
                . code: 105
        """
        company = fake.company_provider()
        department1 = fake.department({'company_id': company.id, 'is_active': True})
        role_title1 = fake.role_title_provider({
            'company_id': company.id, 'department_id': department1.id, 'is_active': True})
        staff = fake.staff_provider({'company_id': company.id, 'is_active': True})
        department_staff = DepartmentStaff(
            department_id=department1.id,
            staff_id=staff.id,
            role_title_id=role_title1.id,
            is_active=True
        )
        with db():
            db.session.add(department_staff)
            db.session.commit()

        department2 = fake.department({'company_id': company.id, 'is_active': True})
        role_title2 = fake.role_title_provider({
            'company_id': company.id, 'department_id': department2.id, 'is_active': True})

        update_dept_staff = {
            "department_id": department2.id,
            "staff_id": staff.id,
            "role_title_id": role_title2.id,
            "is_active": True
        }
        resp = client.put(f"{settings.BASE_API_PREFIX}/departments/staff/update",
                          json=jsonable_encoder(update_dept_staff))
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '105'
        assert 'Staff đã thuộc department khác' in data.get('message')

    def test_134_response_create_staff_id_not_exists(self, client: TestClient):
        """
            Test api PUT update Department Staff response code 134
            Step by step:
            - Tạo company trong DB
            - Tạo department, role_title gắn với company
            - Gọi API Department Update Staff để create với department_id và staff_id chưa tồn tại
            - Đầu ra mong muốn:
                . status code: 400
                . code: 134
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id, 'is_active': True})
        role_title = fake.role_title_provider({
            'company_id': company.id, 'department_id': department.id, 'is_active': True})

        update_dept_staff = {
            "department_id": department.id,
            "staff_id": 1,
            "role_title_id": role_title.id,
            "is_active": True
        }
        resp = client.put(f"{settings.BASE_API_PREFIX}/departments/staff/update",
                          json=jsonable_encoder(update_dept_staff))
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '134'
        assert data.get('message') == 'Id của staff không tồn tại'

    def test_191_response_create_role_title_id_not_exists(self, client: TestClient):
        """
            Test api PUT update Department Staff response code 191
            Step by step:
            - Tạo company trong DB
            - Tạo department, staff gắn với company
            - Gọi API Department Update Staff để create với department_id, staff_id và role_title_id chưa tồn tại
            - Đầu ra mong muốn:
                . status code: 400
                . code: 191
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id, 'is_active': True})
        staff = fake.staff_provider({'company_id': company.id, 'is_active': True})

        update_dept_staff = {
            "department_id": department.id,
            "staff_id": staff.id,
            "role_title_id": 1,
            "is_active": True
        }
        resp = client.put(f"{settings.BASE_API_PREFIX}/departments/staff/update",
                          json=jsonable_encoder(update_dept_staff))
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '191'
        assert data.get('message') == 'role title id không tồn tại'

    def test_191_response_update_with_role_title_id_not_exists(self, client: TestClient):
        """
            Test api PUT update Department Staff response code 191
            Step by step:
            - Tạo company trong DB
            - Tạo department, role_title, staff gắn với company
            - Gán department-staff
            - Gọi API Department Update Staff để update với department_id, staff_id và role_title_id chưa tồn tại
            - Đầu ra mong muốn:
                . status code: 400
                . code: 191
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id, 'is_active': True})
        role_title = fake.role_title_provider({
            'company_id': company.id, 'department_id': department.id, 'is_active': True})
        staff = fake.staff_provider({'company_id': company.id, 'is_active': True})
        department_staff = DepartmentStaff(
            department_id=department.id,
            staff_id=staff.id,
            role_title_id=role_title.id,
            is_active=True
        )
        with db():
            db.session.add(department_staff)
            db.session.commit()

        update_dept_staff = {
            "department_id": department.id,
            "staff_id": staff.id,
            "role_title_id": role_title.id + 1,
            "is_active": True
        }
        resp = client.put(f"{settings.BASE_API_PREFIX}/departments/staff/update",
                          json=jsonable_encoder(update_dept_staff))
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
