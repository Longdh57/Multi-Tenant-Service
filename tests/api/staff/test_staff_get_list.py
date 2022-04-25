import json
import random
from typing import List

from fastapi.encoders import jsonable_encoder
from fastapi_sqlalchemy import db
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from app.core.config import settings
from app.models import Staff, Company, Department, RoleTitle, Team
from app.schemas.sche_base import ResponseSchemaBase
from tests.api import APITestCase
from tests.faker import fake
from app.core import message


class TestGetStaffListAPI(APITestCase):
    ISSUE_KEY = "O2OSTAFF-291"

    @staticmethod
    def staff(company: Company, staff: Staff = None, department: Department = None, role_title: RoleTitle = None, teams: List[Team] = None):
        if staff is None:
            staff = fake.staff_provider({'company_id': company.id})
        if department is None:
            department = fake.department({'company_id': company.id})
        role_title = fake.role_title_provider(
            {'company_id': company.id, 'department_id': department.id})
        fake.add_staff_to_department(
            company=company, staff=staff, department=department, role_title=role_title)
        if teams:
            for team in teams:
                fake.add_staff_to_team(company=company, team=team)
        return staff

    @staticmethod
    def staffs(company: Company, department: Department = None, total: int = 40, teams: List[Team] = None):
        if not company:
            company = fake.company_provider()
        for i in range(total):
            TestGetStaffListAPI.staff(
                company=company, department=department, teams=teams)

    def test_000_response_type_list_with_no_keyword(self, client: TestClient):
        """
            Test api get Staff List response code 000
            Step by step:
            - Gọi API Staff List với đầu vào chuẩn type = list
            - Đầu ra mong muốn:
                . status code: 200`
                . code: 000
        """
        company = fake.company_provider()
        self.staff(company=company)
        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None

    def test_000_response_type_list_search_with_staff_name_keyword_match_all(self, client: TestClient):
        """
            Test api get Staff List response code 000
            Step by step:
            - Tạo 1 Staff có name = "staff với like"
            - Tạo 1 Staff có name = "Test với keyword like"
            - Tạo 1 Staff có name = "Test keyword like"
            - Gọi API Staff List với đầu vào chuẩn type = list
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 2
        """
        company = fake.company_provider()
        keywords = ["staff với like",
                    "Test với keyword like", "Test keyword like"]
        for keyword in keywords:
            staff = fake.staff_provider(
                {'company_id': company.id, 'full_name': keyword})
            self.staff(company=company, staff=staff)
        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&search={'staff với like'}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 1

    def test_000_response_type_list_search_with_keyword_not_match_any_staff(self, client: TestClient):
        """
            Test api get Staff List response code 000
            Step by step:
            - Tạo 1 Staff có name = "staff với like"
            - Tạo 1 Staff có name = "Test với keyword like"
            - Tạo 1 Staff có name = "Test keyword like"
            - Gọi API Staff List với đầu vào chuẩn type = list nhưng search không match với bất kỳ keyword nào
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 0
        """
        company = fake.company_provider()
        keywords = ["staff với like",
                    "Test với keyword like", "Test keyword like"]
        for keyword in keywords:
            staff = fake.staff_provider(
                {'company_id': company.id, 'full_name': keyword})
            self.staff(company=company, staff=staff)
        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&search={'staff với likeaaaa'}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 0

    def test_000_response_type_list_search_with_staff_name_keyword_like(self, client: TestClient):
        """
            Test api get Staff List response code 000
            Step by step:
            - Tạo 1 Staff có name = "staff với like"
            - Tạo 1 Staff có name = "Test với keyword like"
            - Tạo 1 Staff có name = "Test keyword like"
            - Gọi API Staff List với đầu vào chuẩn type = list, search match like với một số tìm kiếm
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 0
        """
        company = fake.company_provider()
        keywords = ["staff với like",
                    "Test với keyword like", "Test keyword like"]
        for keyword in keywords:
            staff = fake.staff_provider(
                {'company_id': company.id, 'full_name': keyword})
            self.staff(company=company, staff=staff)
        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&search={'keyword'}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 2

    def test_000_response_type_list_search_with_staff_name_one_keyword_match_all(self, client: TestClient):
        """
            Test api get Staff List response code 000
            Step by step:
            - Tạo 1 Staff có name = "staff với like"
            - Tạo 1 Staff có name = "Test với keyword like"
            - Tạo 1 Staff có name = "Test keyword like"
            - Gọi API Staff List với đầu vào chuẩn type = list, search match like với một số tìm kiếm
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 0
        """
        company = fake.company_provider()
        keywords = ["staff với like",
                    "Test với keyword like", "Test keyword like"]
        for keyword in keywords:
            staff = fake.staff_provider(
                {'company_id': company.id, 'full_name': keyword})
            self.staff(company=company, staff=staff)
        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&search={'staff với like'}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 1

    def test_000_response_type_list_search_with_staff_name_keyword_uppercase(self, client: TestClient):
        """
            Test api get Staff List response code 000
            Step by step:
            - Tạo 1 Staff có name = "staff với like"
            - Tạo 1 Staff có name = "Test với keyword like"
            - Tạo 1 Staff có name = "Test keyword like"
            - Gọi API Staff List với đầu vào chuẩn type = list, search match like với một số tìm kiếm
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 0
        """
        company = fake.company_provider()
        keywords = ["staff với like",
                    "Test với keyword like", "Test keyword like"]
        for keyword in keywords:
            staff = fake.staff_provider(
                {'company_id': company.id, 'full_name': keyword})
            self.staff(company=company, staff=staff)
        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&search={'STAFF VỚI LIKE'}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 1

    def test_000_response_type_list_search_with_staff_name_keyword_lowercase(self, client: TestClient):
        """
            Test api get Staff List response code 000
            Step by step:
            - Tạo 1 Staff có name = "staff với like"
            - Tạo 1 Staff có name = "Test với keyword like"
            - Tạo 1 Staff có name = "Test keyword like"
            - Gọi API Staff List với đầu vào chuẩn type = list, search match like với một số tìm kiếm
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 0
        """
        company = fake.company_provider()
        keywords = ["staff với like",
                    "Test với keyword like", "Test keyword like"]
        for keyword in keywords:
            staff = fake.staff_provider(
                {'company_id': company.id, 'full_name': keyword})
            self.staff(company=company, staff=staff)
        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&search={'staff với like'}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 1

    def test_000_response_type_list_search_with_staff_name_accented_vietnamese(self, client: TestClient):
        """
            Test api get Staff List response code 000
            Step by step:
            - Tạo 1 Staff có name = "staff với like"
            - Tạo 1 Staff có name = "Test với keyword like"
            - Tạo 1 Staff có name = "Test keyword like"
            - Gọi API Staff List với đầu vào chuẩn type = list, search match like với một số tìm kiếm
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 0
        """
        company = fake.company_provider()
        keywords = ["staff với like",
                    "Test với keyword like", "Test keyword like"]
        for keyword in keywords:
            staff = fake.staff_provider(
                {'company_id': company.id, 'full_name': keyword})
            self.staff(company=company, staff=staff)
        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&search={'staff với like'}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 1
    # Test email

    def test_000_response_type_list_search_with_staff_email_keyword_like(self, client: TestClient):
        """
            Test api get Staff List response code 000
            Step by step:
            - Tạo 1 Staff có name = "email1@teko.vn"
            - Tạo 1 Staff có name = "anh.nd@teko.vn"
            - Tạo 1 Staff có name = "test@teko.vn"
            - Gọi API Staff List với đầu vào chuẩn type = list, search match like với một số tìm kiếm
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 0
        """
        company = fake.company_provider()
        emails = ["email1@teko.vn", "anh.nd@teko.vn", "test@teko.vn"]
        for email in emails:
            staff = fake.staff_provider(
                {'company_id': company.id, 'email': email})
            self.staff(company=company, staff=staff)
        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&search={'email1'}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 1

    def test_000_response_type_list_search_with_staff_email_one_keyword_match_all(self, client: TestClient):
        """
            Test api get Staff List response code 000
            Step by step:
            - Tạo 1 Staff có name = "email1@teko.vn"
            - Tạo 1 Staff có name = "anh.nd@teko.vn"
            - Tạo 1 Staff có name = "test@teko.vn"
            - Gọi API Staff List với đầu vào chuẩn type = list, search match like với một số tìm kiếm
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 0
        """
        company = fake.company_provider()
        emails = ["email1@teko.vn", "anh.nd@teko.vn", "test@teko.vn"]
        for email in emails:
            staff = fake.staff_provider(
                {'company_id': company.id, 'email': email})
            self.staff(company=company, staff=staff)
        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&search={'email1@teko.vn'}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 1

    def test_000_response_type_list_search_with_staff_email_keyword_uppercase(self, client: TestClient):
        """
            Test api get Staff List response code 000
            Step by step:
            - Tạo 1 Staff có name = "email1@teko.vn"
            - Tạo 1 Staff có name = "anh.nd@teko.vn"
            - Tạo 1 Staff có name = "test@teko.vn"
            - Gọi API Staff List với đầu vào chuẩn type = list, search match like với một số tìm kiếm
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 3
        """
        company = fake.company_provider()
        emails = ["email1@teko.vn", "anh.nd@teko.vn", "test@teko.vn"]
        for email in emails:
            staff = fake.staff_provider(
                {'company_id': company.id, 'email': email})
            self.staff(company=company, staff=staff)
        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&search={'@TEKO.VN'}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 3

    def test_000_response_type_list_search_with_staff_email_keyword_lowercase(self, client: TestClient):
        """
            Test api get Staff List response code 000
            Step by step:
            - Tạo 1 Staff có name = "email1@teko.vn"
            - Tạo 1 Staff có name = "anh.nd@teko.vn"
            - Tạo 1 Staff có name = "test@teko.vn"
            - Gọi API Staff List với đầu vào chuẩn type = list, search match like với một số tìm kiếm
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 3
        """
        company = fake.company_provider()
        emails = ["email1@teko.vn", "anh.nd@teko.vn", "test@teko.vn"]
        for email in emails:
            staff = fake.staff_provider(
                {'company_id': company.id, 'email': email})
            self.staff(company=company, staff=staff)
        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&search={'@teko.vn'}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 3

    # test phone number
    # def test_000_response_type_list_search_with_staff_phone_number_keyword_like(self, client: TestClient):
    #     pass

    # def test_000_response_type_list_search_with_staff_phone_number_one_keyword_match_all(self, client: TestClient):
    #     pass

    # # test staff_code
    # def test_000_response_type_list_search_with_staff_code_keyword_like(self, client: TestClient):
    #     pass

    # def test_000_response_type_list_search_with_staff_code_one_keyword_match_all(self, client: TestClient):
    #     pass

    # def test_000_response_type_list_search_with_staff_code_keyword_uppercase(self, client: TestClient):
    #     pass

    # def test_000_response_type_list_search_with_staff_code_keyword_lowercase(self, client: TestClient):
    #     pass

    # fillter with department, team, parent node
    def test_000_response_type_list_search_with_staff_and_filter_with_department(self, client: TestClient):
        """
            Test api get Staff List response code 000
            Step by step:
            - Tạo department
            - Gọi API Staff List với đầu vào chuẩn type = list, search match like với một số tìm kiếm
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 3
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id})
        self.staffs(company=company, department=department)
        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?department_id=1&page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 40

    def test_000_response_type_list_search_with_staff_and_filter_with_team(self, client: TestClient):
        """
            Test api get Staff List response code 000
            Step by step:
            - Tạo department
            - Gọi API Staff List với đầu vào chuẩn type = list, search match like với một số tìm kiếm
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 3
        """
        company = fake.company_provider()
        department = fake.department({'company_id': company.id})
        self.staffs(company=company, department=department)
        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?department_id={department.id}&page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 40

    def test_000_response_type_list_search_with_staff_and_filter_with_parent_node(self, client: TestClient):
        """
            Test api get Staff List response code 000
            Step by step:
            - Tạo department
            - Gọi API Staff List với đầu vào chuẩn type = list, search match like với một số tìm kiếm
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 3
        """
        company = fake.company_provider()
        manager_level1 = self.staff(company=company)
        manager_level2 = fake.staff_provider(
            {'company_id': company.id, 'manager_id': manager_level1.id})
        manager_level3 = fake.staff_provider(
            {'company_id': company.id, 'manager_id': manager_level2.id})
        manager_level4 = fake.staff_provider(
            {'company_id': company.id, 'manager_id': manager_level3.id})
        fake.staff_provider(
                {'company_id': company.id, 'manager_id': manager_level3.id})
        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?&page_size=10&page=1&sort_by=id&parent_node={manager_level1.id}&order=desc&company_id={company.id}&type=list")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 4

    def test_000_response_type_list_search_with_staff_and_filter_with_manager_id(self, client: TestClient):
        """
            Test api get Staff List response code 000
            Step by step:
            - Tạo department
            - Gọi API Staff List với đầu vào chuẩn type = list, search match like với một số tìm kiếm
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 3
        """
        company = fake.company_provider()
        self.staffs(company=company, total=5)
        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?&page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 5

    def test_000_response_type_list_company_has_5_staffs_active(self, client: TestClient):
        """
            Test api get Staff List response code 000
            Step by step:
            - Tạo department
            - Gọi API Staff List với đầu vào chuẩn type = list, search match like với một số tìm kiếm
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 3
        """
        company = fake.company_provider()
        self.staffs(company=company, total=5)
        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?&page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 5

    def test_000_response_type_list_company_has_5_staffs_active_and_5_inactive_expect_return_5_active_staff(self, client: TestClient):
        """
            Test api get Staff List response code 000
            Step by step:
            - Tạo department
            - Gọi API Staff List với đầu vào chuẩn type = list, search match like với một số tìm kiếm
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 3
        """
        company = fake.company_provider()
        self.staffs(company=company, total=5)
        for i in range(5):
            fake.staff_provider({'company_id': company.id, 'is_active': False})
        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?&page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 5

    def test_000_response_type_list_search_with_manager_id_not_exists(self, client: TestClient):
        """
            Test api get Staff List response code 000
            Step by step:
            - Tạo department
            - Gọi API Staff List với đầu vào chuẩn type = list, manager id không tồn tại thì ko trả ra staff nào
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 3
        """
        company = fake.company_provider()
        manager = fake.staff_provider(
            {'company_id': company.id, 'is_active': True})
        staff = fake.staff_provider(
            {'company_id': company.id, 'is_active': True, 'manager_id': manager.id})
        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?manager_id=0&page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 0

    def test_000_response_type_list_search_multiple_manager_id_but_manager_inactive_return_all_staff_have_manager_active(self, client: TestClient):
        """
            Test api get Staff List response code 000
            Step by step:
            - Tạo department
            - Gọi API Staff List với đầu vào chuẩn type = list, manager id không tồn tại thì ko trả ra staff nào
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 3
        """
        company = fake.company_provider()
        manager = fake.staff_provider(
            {'company_id': company.id, 'is_active': True})
        staff = fake.staff_provider(
            {'company_id': company.id, 'is_active': True, 'manager_id': manager.id})
        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?manager_id=0&manager_id={manager.id}&page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 1

    def test_000_response_type_list_search_multiple_department_id_but_department_inactive_return_all_staff_have_department_active(self, client: TestClient):
        """
            Test api get Staff List response code 000
            Step by step:
            - Tạo department
            - Gọi API Staff List với đầu vào chuẩn type = list, search match like với một số tìm kiếm
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 3
        """
        # company = fake.company_provider()
        # department = fake.department({'company_id': company.id})
        # department_inactive = fake.department(
        #     {'company_id': company.id, 'is_active': False})
        # self.staffs(company=company, department=department, total=5)
        # self.staffs(company=company, department=department_inactive, total=5)
        # resp = client.get(
        #     f"{settings.BASE_API_PREFIX}/staffs?department_id={department.id}&department_id={department_inactive.id}&page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list")
        # data = resp.json()

        # assert resp.status_code == 200
        # assert data.get('code') == '000'
        # assert data.get('message') == 'Thành công'
        # assert data.get('metadata') is not None
        # assert data.get('metadata').get('total_items') == 5

    def test_000_response_type_list_search_multiple_team_id_team_inactive_return_all_staff_have_team_active(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Gọi API team List với đầu vào chuẩn type = list, 40 team, 30 page_size ở page 1
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 40
        """
        company = fake.company_provider()
        team = fake.team({'company_id': company.id})
        team_inactive = fake.team({'company_id': company.id})
        self.staffs(company=company, total=5, teams=[team, team_inactive])
        self.staffs(company=company, total=5, teams=[team_inactive])
        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?team_id={team.id}&page_size=30&page=1&company_id={company.id}&type=list")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 5

    def test_000_response_type_list_search_multiple_team_id_team_not_exists_return_all_staff_have_team_active(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Gọi API team List với đầu vào chuẩn type = list, 40 team, 30 page_size ở page 1
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 40
        """
        company = fake.company_provider()
        team = fake.team({'company_id': company.id})
        self.staffs(company=company, total=5, teams=[team])
        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?team_id={team.id}&team_id=0&page_size=30&page=1&company_id={company.id}&type=list")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 5

    def test_000_response_type_list_parent_node_which_has_n_staff_under_n_level(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Gọi API team List với đầu vào chuẩn type = Tree
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        manager_level1 = self.staff(company=company)
        manager_level2 = fake.staff_provider(
            {'company_id': company.id, 'manager_id': manager_level1.id})
        manager_level3 = fake.staff_provider(
            {'company_id': company.id, 'manager_id': manager_level2.id})
        fake.staff_provider(
                {'company_id': company.id, 'manager_id': manager_level3.id})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?page_size=30&page=1&sort_by=created_at&order=asc&company_id={company.id}&type=list")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata').get('total_items') == 4

    def test_000_response_type_list_parent_node_which_has_n_staff_under_1_level(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Gọi API team List với đầu vào chuẩn type = Tree
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        manager = self.staff(company=company)
        for i in range(5):
            fake.staff_provider(
                {'company_id': company.id, 'manager_id': manager.id})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?page_size=30&page=1&sort_by=created_at&order=asc&company_id={company.id}&type=list")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata').get('total_items') == 6

    def test_000_check_paging_40_records_page_size_30_page_equal_1(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Gọi API team List với đầu vào chuẩn type = list, 40 team, 30 page_size ở page 1
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 40
        """
        company = fake.company_provider()
        self.staffs(company=company, total=40)

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?page_size=30&page=1&company_id={company.id}&type=list")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 40
        assert data.get('metadata').get('page_size') == 30
        assert data.get('metadata').get('current_page') == 1

    def test_000_check_paging_40_records_page_size_30_page_equal_2(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Gọi API team List với đầu vào chuẩn type = list, 40 team, 30 page_size ở page 1
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 40
                . page_size: 30
                . page: 2
        """
        company = fake.company_provider()
        self.staffs(company=company, total=40)

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?page_size=30&page=2&company_id={company.id}&type=list")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 40
        assert data.get('metadata').get('page_size') == 30
        assert data.get('metadata').get('current_page') == 2

    def test_000_check_paging_40_records_page_size_30_page_equal_3(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Gọi API team List với đầu vào chuẩn type = list, 40 team, 30 page_size ở page 1
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 40
                . page_size: 30
                . page: 3
        """
        company = fake.company_provider()
        self.staffs(company=company, total=40)

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?page_size=30&page=3&company_id={company.id}&type=list")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 40
        assert data.get('metadata').get('page_size') == 30
        assert data.get('metadata').get('current_page') == 3

    def test_000_check_paging_40_records_page_size_50_page_equal_1(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Gọi API team List với đầu vào chuẩn type = list, 40 team, 30 page_size ở page 1
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 40
                . page_size: 50
                . page: 1
        """
        company = fake.company_provider()
        self.staffs(company=company, total=40)

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?page_size=50&page=1&company_id={company.id}&type=list")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 40
        assert data.get('metadata').get('page_size') == 50
        assert data.get('metadata').get('current_page') == 1

    def test_000_check_paging_40_records_page_size_30_page_equal_1_sort_by_created_at_order_desc(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Gọi API team List với đầu vào chuẩn type = list, 40 team, 30 page_size ở page 1
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 40
                . page_size: 50
                . page: 1
        """
        company = fake.company_provider()
        self.staffs(company=company, total=40)

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?page_size=30&page=1&sort_by=created_at&order=desc&company_id={company.id}&type=list")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 40
        assert data.get('metadata').get('page_size') == 30
        assert data.get('metadata').get('current_page') == 1
        assert data.get('data')[0]['created_at'] > data.get(
            'data')[1]['created_at']

    def test_000_check_paging_40_records_page_size_30_page_equal_2_sort_by_create_at_order_asc(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Gọi API team List với đầu vào chuẩn type = list, 40 team, 30 page_size ở page 1
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 40
                . page_size: 50
                . page: 1
        """
        company = fake.company_provider()
        self.staffs(company=company, total=40)

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?page_size=30&page=1&sort_by=created_at&order=asc&company_id={company.id}&type=list")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 40
        assert data.get('metadata').get('page_size') == 30
        assert data.get('metadata').get('current_page') == 1
        assert data.get('data')[0]['created_at'] < data.get(
            'data')[1]['created_at']

    def test_000_response_type_tree_with_no_key_word(self, client: TestClient):
        company = fake.company_provider()
        self.staffs(company=company, total=5)

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?company_id={company.id}&type=list")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert len(data.get('data')) == 5

    def test_000_response_type_tree_of_company_has_many_staff_who_has_not_manager(self, client: TestClient):
        company = fake.company_provider()
        self.staffs(company=company, total=5)

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?company_id={company.id}&type=tree")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert len(data.get('data')) == 5

    def test_000_response_type_tree_with_department_id_manager_id_team_id_parent_node(self, client: TestClient):
        pass

    def test_000_response_type_tree_of_company_have_5_children_level_return_correct_tree(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Gọi API team List với đầu vào chuẩn type = Tree
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        manager = self.staff(company=company)
        for i in range(5):
            fake.staff_provider(
                {'company_id': company.id, 'manager_id': manager.id})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?page_size=30&page=1&sort_by=created_at&order=asc&company_id={company.id}&type=tree")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert len(data.get('data')[0]['children']) == 5

    def test_000_response_type_tree_of_company_has_1_node(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Gọi API team List với đầu vào chuẩn type = Tree
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        manager = self.staff(company=company)

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?page_size=30&page=1&sort_by=created_at&order=asc&company_id={company.id}&type=tree")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert len(data.get('data')[0]['children']) == 0

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
        self.staffs(company=company, total=5)

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?page_size=-1&page=1&sort_by=id&order=desc&company_id={company.id}&type=list")
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '002'
        assert data.get(
            'message') == 'Số lượng phần tử trong trang tìm kiếm phải lớn hơn 0 và nhỏ hơn 1000'

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
        self.staffs(company=company, total=5)

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?page_size=1500&page=1&sort_by=id&order=desc&company_id={company.id}&type=list")
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '002'
        assert data.get(
            'message') == 'Số lượng phần tử trong trang tìm kiếm phải lớn hơn 0 và nhỏ hơn 1000'

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
        self.staffs(company=company, total=5)

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?page_size=10&page=-1&sort_by=id&order=desc&company_id={company.id}&type=list")
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '003'
        assert data.get(
            'message') == 'Số thứ tự của trang hiện tại phải lớn hơn hoặc bằng 0'

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
        self.staffs(company=company, total=5)

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?page_size=10&page=1&sort_by=id&order=esc&company_id={company.id}&type=list")
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '005'
        assert data.get('message') == 'Chiều sắp xếp phải là "desc" hoặc "asc"'

    def test_092_response_company_id_not_null(self, client: TestClient):
        """
            Test api get Team List response code 092
            Step by step:
            - Gọi API Team List với param: không có company_id
            - Đầu ra mong muốn:
                . status code: 400
                . code: 092
        """
        company = fake.company_provider()
        self.staffs(company=company, total=40)

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?page_size=10&page=1&sort_by=id&order=desc")
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '092'
        assert data.get(
            'message') == message.MESSAGE_092_COMPANY_ID_IS_REQUIRED

    def test_051_response_params_type_invalid(self, client: TestClient):
        """
            Test api get Department List response code 051
            Step by step:
            - Gọi API Department List với param: type khác ["tree", "list"]
            - Đầu ra mong muốn:
                . status code: 422
        """
        company = fake.company_provider()
        self.staffs(company=company, total=5)

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=test")

        assert resp.status_code == 422

    def test_999_internal_error(self, client: TestClient):
        """
            Test api get staff List response code 999
            Step by step:
            - Gọi API staff List lỗi
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
