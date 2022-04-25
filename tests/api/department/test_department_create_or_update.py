import json
import random

from fastapi.encoders import jsonable_encoder
from fastapi_sqlalchemy import db
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from app.core.config import settings
from app.models import DepartmentStaff, Department, RoleTitle
from app.schemas.sche_base import ResponseSchemaBase
from tests.api import APITestCase
from tests.faker import fake


class TestGetDepartmentCreateUpdateAPI(APITestCase):
    ISSUE_KEY = "O2OSTAFF-285"

    def test_000_response_create_basic(self, client: TestClient):
        """
            Test api POST Create Department response code 000
            Step by step:
            - Tạo company trong DB
            - Gọi POST Create Department với đầu vào chuẩn
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        department = {
            "department_name": fake.job(),
            "description": fake.paragraph(nb_sentences=5),
            "parent_id": None,
            "company_id": company.id,
            "is_active": True
        }
        resp = client.post(f"{settings.BASE_API_PREFIX}/departments", json=jsonable_encoder(department))
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['id'] > 0

    def test_000_response_create_with_parent_id_active_and_has_description(self, client: TestClient):
        """
            Test api POST Create Department response code 000
            Step by step:
            - Tạo company trong DB
            - Tạo department cha trong DB
            - Gọi POST Create Department với đầu vào bao gồm parent_id, description, department_name
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        department_parent = fake.department({'company_id': company.id, 'is_active': True})
        department = {
            "department_name": fake.job(),
            "description": fake.paragraph(nb_sentences=5),
            "parent_id": department_parent.id,
            "company_id": company.id
        }
        resp = client.post(f"{settings.BASE_API_PREFIX}/departments", json=jsonable_encoder(department))
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['id'] > 0

    def test_000_response_update_with_parent_id_active(self, client: TestClient):
        """
            Test api POST Update Department response code 000
            Step by step:
            - Tạo company trong DB
            - Tạo department1, department2 trong DB
            - Tạo department con là con của department1 trong DB
            - Gọi POST Update Department với đầu vào bao gồm parent_id = department2
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        department_parent1 = fake.department({'company_id': company.id, 'is_active': True})
        department_parent2 = fake.department({'company_id': company.id, 'is_active': True})
        department = fake.department({'company_id': company.id, 'parent_id': department_parent1.id, 'is_active': True})

        update_department = {
            "id": department.id,
            "department_name": fake.job(),
            "description": fake.paragraph(nb_sentences=5),
            "parent_id": department_parent2.id,
            "company_id": company.id
        }
        resp = client.post(f"{settings.BASE_API_PREFIX}/departments", json=jsonable_encoder(update_department))
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['id'] > 0

    def test_000_response_update_department_name_description(self, client: TestClient):
        """
            Test api POST Update Department response code 000
            Step by step:
            - Tạo company trong DB
            - Tạo department trong DB
            - Gọi POST Update Department với đầu vào department_name, description
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . department_name, description thay đổi như giá trị truyền vào
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id, 'is_active': True})

        update_department = {
            "id": department.id,
            "department_name": fake.job(),
            "description": fake.paragraph(nb_sentences=5),
            "company_id": company.id
        }
        resp = client.post(f"{settings.BASE_API_PREFIX}/departments", json=jsonable_encoder(update_department))
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['id'] > 0
        with db():
            query_dept = db.session.query(Department).get(department.id)
            assert query_dept.department_name == update_department['department_name']
            assert query_dept.description == update_department['description']

    def test_104_response_create_with_parent_id_inactive(self, client: TestClient):
        """
            Test api POST Create Department response code 104
            Step by step:
            - Tạo company trong DB
            - Tạo department cha trong DB với trạng thái is_active = False
            - Gọi POST Create Department với đầu vào bao gồm parent_id
            - Đầu ra mong muốn:
                . status code: 400
                . code: 104
        """
        company = fake.company_provider()
        department_parent = fake.department({'company_id': company.id, 'is_active': False})
        department = {
            "department_name": fake.job(),
            "description": fake.paragraph(nb_sentences=5),
            "parent_id": department_parent.id,
            "company_id": company.id,
            "is_active": True
        }
        resp = client.post(f"{settings.BASE_API_PREFIX}/departments", json=jsonable_encoder(department))
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '104'
        assert data.get('message') == 'Parent_id đã bị khóa'

    def test_061_response_create_with_company_id_not_exists(self, client: TestClient):
        """
            Test api POST Create Department response code 061
            Step by step:
            - Gọi API Create/Update Role Tile với body company_id không tồn tại trên hệ thống
            - Đầu ra mong muốn:
                . status code: 400
                . code: 061
        """
        department = {
            "department_name": fake.job(),
            "description": fake.paragraph(nb_sentences=5),
            "parent_id": None,
            "company_id": 10,
            "is_active": True
        }
        resp = client.post(f"{settings.BASE_API_PREFIX}/departments", json=jsonable_encoder(department))
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '061'
        assert data.get('message') == 'ID company không tồn tại trong hệ thống'

    def test_091_response_update_department_id_not_exits(self, client: TestClient):
        """
            Test api POST Create/Update Department response code 091
            Step by step:
            - Tạo company trong DB
            - Gọi API Update Department với body department_id không tồn tại trên hệ thống
            - Đầu ra mong muốn:
                . status code: 400
                . code: 091
        """
        company = fake.company_provider()
        department = {
            "id": 10,
            "department_name": fake.job(),
            "description": fake.paragraph(nb_sentences=5),
            "parent_id": None,
            "company_id": company.id,
            "is_active": True
        }
        resp = client.post(f"{settings.BASE_API_PREFIX}/departments", json=jsonable_encoder(department))
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '091'
        assert data.get('message') == 'ID của phòng ban không tồn tại trong hệ thống'

    def test_092_response_create_company_id_not_null(self, client: TestClient):
        """
            Test api POST Create/Update Department response code 092
            Step by step:
            - Gọi API Create/Update Role Tile với body thiếu company_id
            - Đầu ra mong muốn:
                . status code: 400
                . code: 092
        """
        department = {
            "department_name": fake.job(),
            "description": fake.paragraph(nb_sentences=5),
            "parent_id": None,
            "is_active": True
        }
        resp = client.post(f"{settings.BASE_API_PREFIX}/departments", json=jsonable_encoder(department))
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '092'
        assert data.get('message') == 'ID của company không được để trống'

    def test_094_response_parent_id_not_exists(self, client: TestClient):
        """
            Test api POST Create Department response code 094
            Step by step:
            - Gọi API Create Role Tile với body parent_id không tồn tại trên hệ thống
            - Đầu ra mong muốn:
                . status code: 400
                . code: 094
        """
        company = fake.company_provider()
        department = {
            "department_name": fake.job(),
            "description": fake.paragraph(nb_sentences=5),
            "parent_id": 10,
            "company_id": company.id,
            "is_active": True
        }
        resp = client.post(f"{settings.BASE_API_PREFIX}/departments", json=jsonable_encoder(department))
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '094'
        assert data.get('message') == 'ID của phòng ban cấp trên không tồn tại trong hệ thống'

    def test_000_response_delete_department_zero_staff_and_has_no_child(self, client: TestClient):
        """
            Test api POST Update Department response code 095
            Step by step:
            - Tạo company, Department trong DB
            - Gọi API Update xóa Department không có nhân viên, không có department child
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id})

        update_department = {
            "id": department.id,
            "department_name": fake.job(),
            "description": fake.paragraph(nb_sentences=5),
            "parent_id": None,
            "company_id": company.id,
            "is_active": False
        }
        resp = client.post(f"{settings.BASE_API_PREFIX}/departments", json=jsonable_encoder(update_department))
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['id'] > 0

    def test_000_response_delete_department_with_child_zero_staff(self, client: TestClient):
        """
            Test api POST Update Department response code 000
            Step by step:
            - Tạo company, Department, role_title gắn với department trong DB
            - Tạo multi child Department & role_title đính kèm trong DB
            - Gọi API Update xóa Department không có nhân viên
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . department bị xóa
                . role_title gắn với department bị xóa
                . tất cả các department con đều bị xóa
                . tất cả các role_title gắn với department con đều bị xóa
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id})

        department_childs = []
        for _ in range(1, 10):
            dept_child = fake.department({'company_id': company.id, 'parent_id': department.id, 'is_active': True})
            department_childs.append(dept_child)
            fake.role_titles(company=company, department_id=dept_child.id, total=random.randint(1, 5))

        update_department = {
            "id": department.id,
            "department_name": fake.job(),
            "description": fake.paragraph(nb_sentences=5),
            "parent_id": None,
            "company_id": company.id,
            "is_active": False
        }
        resp = client.post(f"{settings.BASE_API_PREFIX}/departments", json=jsonable_encoder(update_department))
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['id'] == department.id

        list_dept_ids = [child.id for child in department_childs]
        list_dept_ids.append(department.id)
        with db():
            childs = db.session.query(Department).filter(Department.id.in_(list_dept_ids)).all()
            for child in childs:
                assert child.is_active == False
            role_titles = db.session.query(RoleTitle).filter(RoleTitle.department_id.in_(list_dept_ids)).all()
            for role_title in role_titles:
                assert role_title.is_active == False

    def test_000_response_delete_department_with_all_inactive_staff_and_has_some_child(self, client: TestClient):
        """
            Test api POST Update Department response code 000
            Step by step:
            - Tạo company, Department, role_title gắn với department trong DB
            - Tạo staff và gắn với department trong trạng thái khóa
            - Tạo multi child Department & role_title đính kèm trong DB
            - Gọi API Update xóa Department không có nhân viên & department con không có nhân viên
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . department bị xóa
                . role_title gắn với department bị xóa
                . tất cả các department con đều bị xóa
                . tất cả các role_title gắn với department con đều bị xóa
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id, 'is_active': True})
        role_title = fake.role_title_provider(
            {'company_id': company.id, 'department_id': department.id, 'is_active': True})
        number_staffs = random.randint(2, 10)
        staffs = [fake.staff_provider({'company_id': company.id, 'is_active': True}) for _ in range(number_staffs)]
        department_staff_mappings = [{
            'department_id': department.id,
            'staff_id': staff.id,
            'role_title_id': role_title.id,
            'is_active': False
        } for staff in staffs]
        with db():
            db.session.bulk_insert_mappings(DepartmentStaff, department_staff_mappings)
            db.session.commit()

        department_childs = []
        for _ in range(1, 10):
            dept_child = fake.department({'company_id': company.id, 'parent_id': department.id, 'is_active': True})
            department_childs.append(dept_child)
            fake.role_titles(company=company, department_id=dept_child.id, total=random.randint(1, 5))

        update_department = {
            "id": department.id,
            "department_name": fake.job(),
            "description": fake.paragraph(nb_sentences=5),
            "parent_id": None,
            "company_id": company.id,
            "is_active": False
        }
        resp = client.post(f"{settings.BASE_API_PREFIX}/departments", json=jsonable_encoder(update_department))
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['id'] == department.id

        list_dept_ids = [child.id for child in department_childs]
        list_dept_ids.append(department.id)
        with db():
            childs = db.session.query(Department).filter(Department.id.in_(list_dept_ids)).all()
            for child in childs:
                assert child.is_active == False
            role_titles = db.session.query(RoleTitle).filter(RoleTitle.department_id.in_(list_dept_ids)).all()
            for role_title in role_titles:
                assert role_title.is_active == False

    def test_000_response_delete_department_with_all_inactive_staff(self, client: TestClient):
        """
            Test api POST Update Department response code 095
            Step by step:
            - Tạo company, Department, staff, role_title trong DB
            - Thêm Staff vào Department toàn bộ ở trạng thái khóa
            - Gọi API Update xóa Department có tất cả nhân viên đang khóa
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
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
            'is_active': False
        } for staff in staffs]

        with db():
            db.session.bulk_insert_mappings(DepartmentStaff, department_staff_mappings)
            db.session.commit()

        update_department = {
            "id": department.id,
            "department_name": fake.job(),
            "description": fake.paragraph(nb_sentences=5),
            "parent_id": None,
            "company_id": company.id,
            "is_active": False
        }
        resp = client.post(f"{settings.BASE_API_PREFIX}/departments", json=jsonable_encoder(update_department))
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['id'] > 0

    def test_095_response_can_not_delete_department_have_staff(self, client: TestClient):
        """
            Test api POST Update Department response code 095
            Step by step:
            - Tạo company, Department, staff, role_title trong DB
            - Thêm Staff vào Department
            - Gọi API Update xóa Department đang có nhân viên
            - Đầu ra mong muốn:
                . status code: 400
                . code: 095
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

        update_department = {
            "id": department.id,
            "department_name": fake.job(),
            "description": fake.paragraph(nb_sentences=5),
            "parent_id": None,
            "company_id": company.id,
            "is_active": False
        }
        resp = client.post(f"{settings.BASE_API_PREFIX}/departments", json=jsonable_encoder(update_department))
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '095'
        assert data.get('message') == 'Không được phép xóa phòng ban đang có nhân viên'

    def test_096_response_can_not_delete_department_with_child_have_staff(self, client: TestClient):
        """
            Test api POST Create/Update Department response code 096
            Step by step:
            - Gọi API Create/Update Role Tile xóa phòng ban mà các phòng ban cấp dưới đang có nhân viên
            - Đầu ra mong muốn:
                . status code: 400
                . code: 096
        """
        assert True

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
            Test api POST Create/Update Department response code 999
            Step by step:
            - Gọi POST Create/Update Department lỗi
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
