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


class TestGetRoleTitleCreateUpdateAPI(APITestCase):
    ISSUE_KEY = "O2OSTAFF-290"

    def test_000_response_create_job_title_with_require_field(self, client: TestClient):
        """
            Test api Post Create Role Tile response code 000
            Step by step:
            - Tạo company trong DB
            - Gọi API Post Create Role Tile với đầu vào chuẩn
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()

        role_title = {
            "role_title_name": fake.job(),
            "description": fake.paragraph(nb_sentences=5),
            "company_id": company.id,
            "department_id": None,
            "is_active": True
        }
        resp = client.post(f"{settings.BASE_API_PREFIX}/role_titles", json=jsonable_encoder(role_title))
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['id'] > 0

    def test_000_response_create_with_department_id(self, client: TestClient):
        """
            Test api Post Create Role Tile response code 000
            Step by step:
            - Tạo company, department trong DB
            - Gọi API Post Create Role Tile với đầu vào chuẩn có chứa department_id
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id, 'is_active': True})

        role_title = {
            "role_title_name": fake.job(),
            "description": fake.paragraph(nb_sentences=5),
            "company_id": company.id,
            "department_id": department.id,
            "is_active": True
        }
        resp = client.post(f"{settings.BASE_API_PREFIX}/role_titles", json=jsonable_encoder(role_title))
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['id'] > 0

    def test_000_response_create_with_same_name_in_a_department(self, client: TestClient):
        """
            Test api Post Create Role Tile response code 196
            Step by step:
            - Tạo company, department trong DB
            - Tạo role_title gắn với department trong DB
            - Gọi API Post Create Role Tile với đầu vào role_title_name giống role_title đã tồn tại
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id, 'is_active': True})
        fake.role_title_provider({
            'role_title_name': 'Chức danh test',
            'company_id': company.id,
            'department_id': department.id,
            'is_active': True
        })

        role_title = {
            "role_title_name": 'Chức danh test',
            "description": fake.paragraph(nb_sentences=5),
            "company_id": company.id,
            "department_id": department.id,
            "is_active": True
        }
        resp = client.post(f"{settings.BASE_API_PREFIX}/role_titles", json=jsonable_encoder(role_title))
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['id'] > 0

    def test_000_response_create_with_same_name_in_diff_department(self, client: TestClient):
        """
            Test api Post Create Role Tile response code 196
            Step by step:
            - Tạo company, department1 trong DB
            - Tạo role_title gắn với department1 trong DB
            - Tạo department2 trong DB
            - Gọi API Post Create Role Tile với name giống role_title đã tồn tại nhưng department_id = department2
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        department1 = fake.department({'company_id': company.id, 'is_active': True})
        fake.role_title_provider({
            'role_title_name': 'Chức danh test',
            'company_id': company.id,
            'department_id': department1.id,
            'is_active': True
        })

        department2 = fake.department({'company_id': company.id, 'is_active': True})
        role_title = {
            "role_title_name": 'Chức danh test',
            "description": fake.paragraph(nb_sentences=5),
            "company_id": company.id,
            "department_id": department2.id,
            "is_active": True
        }
        resp = client.post(f"{settings.BASE_API_PREFIX}/role_titles", json=jsonable_encoder(role_title))
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['id'] > 0

    def test_000_response_update_re_active_role_title_in_department(self, client: TestClient):
        """
            Test api Post Create Role Tile response code 196
            Step by step:
            - Tạo company, department trong DB
            - Tạo role_title gắn với department nhưng ở trạng thái inactive trong DB
            - Gọi API Post Update Role Tile với is_active = True
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id, 'is_active': True})
        role_title = fake.role_title_provider({
            'role_title_name': fake.job(),
            'company_id': company.id,
            'department_id': department.id,
            'is_active': False
        })

        update_role_title = {
            "id": role_title.id,
            "role_title_name": fake.job(),
            "description": fake.paragraph(nb_sentences=5),
            "company_id": company.id,
            "department_id": department.id,
            "is_active": True
        }
        resp = client.post(f"{settings.BASE_API_PREFIX}/role_titles", json=jsonable_encoder(update_role_title))
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['id'] == role_title.id

    def test_197_response_update_re_active_role_title_in_department_inactive(self, client: TestClient):
        """
            Test api Post Create Role Tile response code 196
            Step by step:
            - Tạo company trong DB
            - Tạo department ở trạng thái inactive trong DB
            - Tạo role_title gắn với department ở trạng thái inactive trong DB
            - Gọi API Post Update Role Tile với is_active = True
            - Đầu ra mong muốn:
                . status code: 400
                . code: 197
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id, 'is_active': False})
        role_title = fake.role_title_provider({
            'role_title_name': fake.job(),
            'company_id': company.id,
            'department_id': department.id,
            'is_active': False
        })

        update_role_title = {
            "id": role_title.id,
            "role_title_name": fake.job(),
            "description": fake.paragraph(nb_sentences=5),
            "company_id": company.id,
            "department_id": department.id,
            "is_active": True
        }
        resp = client.post(f"{settings.BASE_API_PREFIX}/role_titles", json=jsonable_encoder(update_role_title))
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '197'
        assert data.get('message') == 'Không thể kích hoạt role_title trong phòng ban đã khóa'

    def test_061_response_company_id_not_exits(self, client: TestClient):
        """
            Test api Post Create Role Tile response code 061
            Step by step:
            - Gọi API Create Role Tile với body company_id không tồn tại trên hệ thống
            - Đầu ra mong muốn:
                . status code: 400
                . code: 061
        """
        role_title = {
            "role_title_name": fake.job(),
            "description": fake.paragraph(nb_sentences=5),
            "company_id": 10,
            "department_id": None,
            "is_active": True
        }
        resp = client.post(f"{settings.BASE_API_PREFIX}/role_titles", json=jsonable_encoder(role_title))
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '061'
        assert data.get('message') == 'ID company không tồn tại trong hệ thống'

    def test_091_response_create_department_id_not_exits(self, client: TestClient):
        """
            Test api Post Create Role Tile response code 091
            Step by step:
            - Tạo company trong DB
            - Gọi API Create Role Tile với body department_id không tồn tại trên hệ thống
            - Đầu ra mong muốn:
                . status code: 400
                . code: 091
        """
        company = fake.company_provider()
        role_title = {
            "role_title_name": fake.job(),
            "description": fake.paragraph(nb_sentences=5),
            "company_id": company.id,
            "department_id": 10,
            "is_active": True
        }
        resp = client.post(f"{settings.BASE_API_PREFIX}/role_titles", json=jsonable_encoder(role_title))
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '091'
        assert data.get('message') == 'ID của phòng ban không tồn tại trong hệ thống'

    def test_192_response_create_department_not_belong_to_company(self, client: TestClient):
        """
            Test api Post Create Role Tile response code 192
            Step by step:
            - Tạo company, department trong DB
            - Gọi API Create Role Tile với body department_id không thuộc company_id
            - Đầu ra mong muốn:
                . status code: 400
                . code: 192
        """
        company1 = fake.company_provider()
        company2 = fake.company_provider()
        department = fake.department({'company_id': company2.id, 'is_active': True})
        role_title = {
            "role_title_name": fake.job(),
            "description": fake.paragraph(nb_sentences=5),
            "company_id": company1.id,
            "department_id": department.id,
            "is_active": True
        }
        resp = client.post(f"{settings.BASE_API_PREFIX}/role_titles", json=jsonable_encoder(role_title))
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '192'
        assert data.get('message') == 'Phòng ban không thuộc trong công ty'

    def test_193_response_update_can_not_disable_role_title(self, client: TestClient):
        """
            Test api Post Update Role Tile response code 193
            Step by step:
            - Tạo company, department, staff, role title trong DB
            - Gán staff với department qua role title
            - Gọi API Update Role Tile với body is_active = False nhưng gắn với department-staff vẫn đang active
            - Đầu ra mong muốn:
                . status code: 400
                . code: 193
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id})
        staffs = [fake.staff_provider({'company_id': company.id, 'is_active': True}) for _ in
                  range(random.randint(2, 10))]
        role_title = fake.role_title_provider(
            {'company_id': company.id, 'department_id': department.id, 'is_active': True})

        department_staff_mappings = [{
            'department_id': department.id,
            'staff_id': staff.id,
            'role_title_id': role_title.id,
            'is_active': True
        } for staff in staffs]
        with db():
            db.session.bulk_insert_mappings(DepartmentStaff, department_staff_mappings)
            db.session.commit()

        update_role_title = {
            "id": role_title.id,
            "role_title_name": fake.job(),
            "company_id": company.id,
            "is_active": False
        }
        resp = client.post(f"{settings.BASE_API_PREFIX}/role_titles", json=jsonable_encoder(update_role_title))
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '193'
        assert data.get('message') == 'Không thể khóa vì job title đang gắn với nhân viên trong phòng ban'

    def test_000_response_update_delete_role_title_with_all_department_staff_inactive(self, client: TestClient):
        """
            Test api Post Update Role Tile response code 000
            Step by step:
            - Tạo company, department, staff, role title trong DB
            - Gán staff với department qua role title
            - Gọi API Update Role Tile với body is_active = False & đang gắn với tất cả department-staff đang inactive
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id})
        staffs = [fake.staff_provider({'company_id': company.id, 'is_active': True}) for _ in
                  range(random.randint(2, 10))]
        role_title = fake.role_title_provider(
            {'company_id': company.id, 'department_id': department.id, 'is_active': True})

        department_staff_mappings = [{
            'department_id': department.id,
            'staff_id': staff.id,
            'role_title_id': role_title.id,
            'is_active': False
        } for staff in staffs]
        with db():
            db.session.bulk_insert_mappings(DepartmentStaff, department_staff_mappings)
            db.session.commit()

        update_role_title = {
            "id": role_title.id,
            "role_title_name": fake.job(),
            "company_id": company.id,
            "is_active": False
        }
        resp = client.post(f"{settings.BASE_API_PREFIX}/role_titles", json=jsonable_encoder(update_role_title))
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['id'] > 0

    def test_194_response_can_not_update_role_title_department(self, client: TestClient):
        """
            Test api Post Update Role Tile response code 194
            Step by step:
            - Tạo company, department1, department2 trong DB
            - Gọi API Create Role Tile với body department_id = department1
            - Gọi API Update Role Tile với body department_id khác department1 => department2
            - Đầu ra mong muốn:
                . status code: 400
                . code: 194
        """
        company = fake.company_provider()
        department1 = fake.department({'company_id': company.id, 'is_active': True})
        department2 = fake.department({'company_id': company.id, 'is_active': True})
        role_title = {
            "role_title_name": fake.job(),
            "description": fake.paragraph(nb_sentences=5),
            "company_id": company.id,
            "department_id": department1.id,
            "is_active": True
        }
        create_resp = client.post(f"{settings.BASE_API_PREFIX}/role_titles", json=jsonable_encoder(role_title))
        create_data = create_resp.json()

        update_role_title = {
            "id": create_data.get('data')['id'],
            "role_title_name": fake.job(),
            "description": fake.paragraph(nb_sentences=5),
            "company_id": company.id,
            "department_id": department2.id,
            "is_active": True
        }
        resp = client.post(f"{settings.BASE_API_PREFIX}/role_titles", json=jsonable_encoder(update_role_title))
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '194'
        assert data.get('message') == 'Không thể cập nhật phòng ban của job title đã tồn tại'

    def test_195_response_update_can_not_update_role_title_company(self, client: TestClient):
        """
            Test api Post Update Role Tile response code 195
            Step by step:
            - Tạo company1, company2 trong DB
            - Gọi API Create Role Tile với body company_id = company1
            - Gọi API Update Role Tile với body company_id khác company_id hiện tại => company2
            - Đầu ra mong muốn:
                . status code: 400
                . code: 195
        """
        company1 = fake.company_provider()
        company2 = fake.company_provider()
        role_title = {
            "role_title_name": fake.job(),
            "description": fake.paragraph(nb_sentences=5),
            "company_id": company1.id,
            "department_id": None,
            "is_active": True
        }
        create_resp = client.post(f"{settings.BASE_API_PREFIX}/role_titles", json=jsonable_encoder(role_title))
        create_data = create_resp.json()

        update_role_title = {
            "id": create_data.get('data')['id'],
            "role_title_name": fake.job(),
            "description": fake.paragraph(nb_sentences=5),
            "company_id": company2.id,
            "department_id": None,
            "is_active": True
        }
        resp = client.post(f"{settings.BASE_API_PREFIX}/role_titles", json=jsonable_encoder(update_role_title))
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '195'
        assert data.get('message') == 'Không thể cập nhật công ty của job title đã tồn tại'

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
