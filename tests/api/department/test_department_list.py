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


class TestGetDepartmentListAPI(APITestCase):
    ISSUE_KEY = "O2OSTAFF-283"

    def test_000_response_normal_type_list(self, client: TestClient):
        """
            Test api get Department List response code 000
            Step by step:
            - Gọi API Department List với đầu vào chuẩn type = list
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        fake.departments(company=company)

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/departments?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') <= 1000

    def test_000_response_normal_type_list_search_with_department_name_keyword_match_all(self, client: TestClient):
        """
            Test api get Department List response code 000
            Step by step:
            - Tạo 2 Deparment có name = "Department với keyword match all"
            - Gọi API Department List với đầu vào chuẩn type = list
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 2
        """
        company = fake.company_provider()
        keyword = 'Department với keyword match all'
        fake.department({'company_id': company.id, 'department_name': keyword, 'is_active': True})
        fake.department({'company_id': company.id, 'department_name': keyword, 'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/departments?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&department_name={keyword}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 2

    def test_000_response_normal_type_list_search_with_department_name_keyword_like(self, client: TestClient):
        """
            Test api get Department List response code 000
            Step by step:
            - Tạo 1 Deparment có name = "Department với like"
            - Tạo 1 Deparment có name = "Test với keyword like"
            - Tạo 1 Deparment có name = "Test keyword like"
            - Gọi API Department List với đầu vào chuẩn type = list, department_name = "với"
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 2
        """
        company = fake.company_provider()
        fake.department({'company_id': company.id, 'department_name': 'Department với like', 'is_active': True})
        fake.department({'company_id': company.id, 'department_name': 'Test với keyword like', 'is_active': True})
        fake.department({'company_id': company.id, 'department_name': 'Test keyword like', 'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/departments?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&department_name={'với'}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 2

    def test_000_response_normal_type_list_search_with_department_name_not_match_any_depart(self, client: TestClient):
        """
            Test api get Department List response code 000
            Step by step:
            - Tạo 1 Deparment có name = "Department với like"
            - Tạo 1 Deparment có name = "Test với keyword like"
            - Tạo 1 Deparment có name = "Test keyword like"
            - Gọi API Department List với đầu vào chuẩn type = list, department_name = "Không match"
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 0
        """
        company = fake.company_provider()
        fake.department({'company_id': company.id, 'department_name': 'Department với like', 'is_active': True})
        fake.department({'company_id': company.id, 'department_name': 'Test với keyword like', 'is_active': True})
        fake.department({'company_id': company.id, 'department_name': 'Test keyword like', 'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/departments?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&department_name={'Không match'}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 0

    def test_000_response_normal_type_list_search_with_department_name_one_keyword_match_all(self, client: TestClient):
        """
            Test api get Department List response code 000
            Step by step:
            - Tạo 1 Deparment có name = "Department với like"
            - Tạo 1 Deparment có name = "Test với keyword like"
            - Tạo 1 Deparment có name = "Với match"
            - Gọi API Department List với đầu vào chuẩn type = list, department_name = "với"
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 3
        """
        company = fake.company_provider()
        fake.department({'company_id': company.id, 'department_name': 'Department với like', 'is_active': True})
        fake.department({'company_id': company.id, 'department_name': 'Test với keyword like', 'is_active': True})
        fake.department({'company_id': company.id, 'department_name': 'Với match', 'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/departments?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&department_name={'với'}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 3

    def test_000_response_normal_type_list_search_with_department_name_keyword_uppercase(self, client: TestClient):
        """
            Test api get Department List response code 000
            Step by step:
            - Tạo 1 Deparment có name = "Department với like"
            - Tạo 1 Deparment có name = "Test với keyword like"
            - Tạo 1 Deparment có name = "Với match"
            - Gọi API Department List với đầu vào chuẩn type = list, department_name = "VỚI"
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 3
        """
        company = fake.company_provider()
        fake.department({'company_id': company.id, 'department_name': 'Department với like', 'is_active': True})
        fake.department({'company_id': company.id, 'department_name': 'Test với keyword like', 'is_active': True})
        fake.department({'company_id': company.id, 'department_name': 'Với match', 'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/departments?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&department_name={'VỚI'}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 3

    def test_000_response_normal_type_list_search_with_department_name_keyword_lowercase(self, client: TestClient):
        """
            Test api get Department List response code 000
            Step by step:
            - Tạo 1 Deparment có name = "Department với like"
            - Tạo 1 Deparment có name = "Test với keyword like"
            - Tạo 1 Deparment có name = "Với match"
            - Gọi API Department List với đầu vào chuẩn type = list, department_name = "với"
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 3
        """
        company = fake.company_provider()
        fake.department({'company_id': company.id, 'department_name': 'Department với like', 'is_active': True})
        fake.department({'company_id': company.id, 'department_name': 'Test với keyword like', 'is_active': True})
        fake.department({'company_id': company.id, 'department_name': 'Với match', 'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/departments?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&department_name={'với'}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 3

    def test_000_response_normal_type_tree(self, client: TestClient):
        """
            Test api get Department List response code 000
            Step by step:
            - Tạo Department cấp 1
            - Tạo Department cấp 2 là con của department cấp 1
            - Tạo Department cấp 3  là con của department cấp 2
            - Gọi API Department List với đầu vào chuẩn type = tree
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . department cấp 1 có child là department cấp 2
                . department cấp 2 có child là department cấp 3
        """
        company = fake.company_provider()
        department_1 = fake.department({'company_id': company.id, 'is_active': True})
        department_2 = fake.department({'company_id': company.id, 'parent_id': department_1.id, 'is_active': True})
        department_3 = fake.department({'company_id': company.id, 'parent_id': department_2.id, 'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/departments?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=tree")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')[0]['department']['department_name'] == department_1.department_name
        assert data.get('data')[0]['children'][0]['department']['department_name'] == department_2.department_name
        assert data.get('data')[0]['children'][0]['children'][0]['department'][
                   'department_name'] == department_3.department_name

    def test_000_response_type_list_company_has_5_departments_active(self, client: TestClient):
        """
            Test api get Department List response code 000
            Step by step:
            - Tạo company và 5 department tương ứng
            - Gọi API Department List với đầu vào chuẩn type = list
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 5
        """
        company = fake.company_provider()
        total_dept = 5
        for _ in range(total_dept):
            fake.department({'company_id': company.id, 'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/departments?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == total_dept

    def test_000_response_type_list_company_has_5_departments_active_and_5_inactive(self, client: TestClient):
        """
            Test api get Department List response code 000
            Step by step:
            - Tạo company và 10 department tương ứng, trong đó 5 active, 5 inactive
            - Gọi API Department List với đầu vào chuẩn type = list
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 5
        """
        company = fake.company_provider()
        total_dept = 10
        for i in range(total_dept):
            fake.department({'company_id': company.id, 'is_active': (i < 5)})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/departments?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 5

    def test_000_response_type_list_search_with_department_name_accented_vietnamese(self, client: TestClient):
        """
            Test api get Department List response code 000 tiếng việt có dấu
            Step by step:
            - Tạo department với tên có dấu
            - Gọi API Department List với đầu vào chuẩn type = list; department_name có dấu
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        name_with_accented_vn = 'Phòng ban có dấu'
        fake.department({'company_id': company.id, 'department_name': name_with_accented_vn, 'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/departments?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&department_name={name_with_accented_vn}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert len(data.get('data')) == 1

    def test_000_response_type_list_search_with_parent_id_not_exists(self, client: TestClient):
        """
            Test api get Department List response code 000 parent_id không tồn tại
            Step by step:
            - Tạo department cha
            - Tạo department con
            - Gọi API Department List với đầu vào chuẩn type = list; parent_id là id không tồn tại
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        department_parent = fake.department({'company_id': company.id})
        fake.department({'company_id': company.id, 'parent_id': department_parent.id, 'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/departments?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&parent_id={department_parent.id + 1}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert len(data.get('data')) == 0

    def test_000_response_type_list_search_with_parent_have_5_child(self, client: TestClient):
        """
            Test api get Department List response code 000 parent_id có 5 items
            Step by step:
            - Tạo department cha
            - Tạo 5 department con tương ứng
            - Gọi API Department List với đầu vào chuẩn type = list; parent_id là id department cha
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        department_parent = fake.department({'company_id': company.id})
        for _ in range(5):
            fake.department({'company_id': company.id, 'parent_id': department_parent.id, 'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/departments?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&parent_id={department_parent.id}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert len(data.get('data')) == 5

    def test_000_response_type_list_search_with_parent_has_no_child(self, client: TestClient):
        """
            Test api get Department List response code 000 parent_id có 5 items
            Step by step:
            - Tạo department cha
            - Gọi API Department List với đầu vào chuẩn type = list; parent_id là id department cha
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 0
        """
        company = fake.company_provider()
        department_parent = fake.department({'company_id': company.id})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/departments?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&parent_id={department_parent.id}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert len(data.get('data')) == 0

    def test_000_check_staff_count_of_department_with_count_staffs(self, client: TestClient):
        """
            Test api get Department List response code 000 check count staff
            Step by step:
            - Tạo 2 department
            - Tạo role_title gắn với department2, staffs gắn với department2
            - Gọi API Department List với đầu vào chuẩn type = list
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . department1 return count_staffs = 0
                . department2 return count_staffs = số staff đã gán
        """
        company = fake.company_provider()
        department1 = fake.department({'company_id': company.id, 'is_active': True})

        department2 = fake.department({'company_id': company.id, 'is_active': True})
        role_title = fake.role_title_provider(
            {'company_id': company.id, 'department_id': department2.id, 'is_active': True})
        number_staffs = random.randint(2, 10)
        staffs = [fake.staff_provider({'company_id': company.id, 'is_active': True}) for _ in range(number_staffs)]
        department_staff_mappings = [{
            'department_id': department2.id,
            'staff_id': staff.id,
            'role_title_id': role_title.id,
            'is_active': True
        } for staff in staffs]
        with db():
            db.session.bulk_insert_mappings(DepartmentStaff, department_staff_mappings)
            db.session.commit()

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/departments?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert len(data.get('data')) == 2
        assert data.get('data')[1]['count_staffs'] == 0 and data.get('data')[1]['id'] == department1.id
        assert data.get('data')[0]['count_staffs'] == number_staffs and data.get('data')[0]['id'] == department2.id

    def test_002_response_page_size_smaller_than_0(self, client: TestClient):
        """
            Test api get Department List response code 002
            Step by step:
            - Tạo 1 list Department trong DB
            - Gọi API Department List với param: page_size < 0
            - Đầu ra mong muốn:
                . status code: 400
                . code: 002
        """
        company = fake.company_provider()
        fake.departments(company=company)

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/departments?page_size=-1&page=1&sort_by=id&order=desc&company_id={company.id}&type=list")
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '002'
        assert data.get('message') == 'Số lượng phần tử trong trang tìm kiếm phải lớn hơn 0 và nhỏ hơn 1000'

    def test_002_response_page_size_lagger_than_1000(self, client: TestClient):
        """
            Test api get Department List response code 002
            Step by step:
            - Tạo 1 list Department trong DB
            - Gọi API Department List với param: page_size > 1000
            - Đầu ra mong muốn:
                . status code: 400
                . code: 002
        """
        company = fake.company_provider()
        fake.departments(company=company)

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/departments?page_size=1500&page=1&sort_by=id&order=desc&company_id={company.id}&type=list")
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '002'
        assert data.get('message') == 'Số lượng phần tử trong trang tìm kiếm phải lớn hơn 0 và nhỏ hơn 1000'

    def test_003_response_page_larger_than_0(self, client: TestClient):
        """
            Test api get Department List response code 003
            Step by step:
            - Gọi API Department List với param: page < 0
            - Đầu ra mong muốn:
                . status code: 400
                . code: 003
        """
        company = fake.company_provider()
        fake.departments(company=company)

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/departments?page_size=10&page=-1&sort_by=id&order=desc&company_id={company.id}&type=list")
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '003'
        assert data.get('message') == 'Số thứ tự của trang hiện tại phải lớn hơn hoặc bằng 0'

    def test_005_response_order_invalid(self, client: TestClient):
        """
            Test api get Department List response code 005
            Step by step:
            - Gọi API Department List với param: order không phải là asc|desc
            - Đầu ra mong muốn:
                . status code: 400
                . code: 005
        """
        company = fake.company_provider()
        fake.departments(company=company)

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/departments?page_size=10&page=1&sort_by=id&order=esc&company_id={company.id}&type=list")
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '005'
        assert data.get('message') == 'Chiều sắp xếp phải là "desc" hoặc "asc"'

    def test_092_response_company_id_not_null(self, client: TestClient):
        """
            Test api get Department List response code 092
            Step by step:
            - Gọi API Department List với param: không có company_id
            - Đầu ra mong muốn:
                . status code: 400
                . code: 092
        """
        company = fake.company_provider()
        fake.departments(company=company)

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/departments?page_size=10&page=1&sort_by=id&order=desc&type=list")
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '092'
        assert data.get('message') == 'ID của company không được để trống'

    def test_051_response_params_type_invalid(self, client: TestClient):
        """
            Test api get Department List response code 051
            Step by step:
            - Gọi API Department List với param: type khác ["tree", "list"]
            - Đầu ra mong muốn:
                . status code: 422
        """
        company = fake.company_provider()
        fake.departments(company=company)

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/departments?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=test")

        assert resp.status_code == 422

    def test_999_internal_error(self, client: TestClient):
        """
            Test api get Department List response code 999
            Step by step:
            - Gọi API Department List lỗi
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
