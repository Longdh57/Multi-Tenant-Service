from app.helpers.enums import StaffContractType
from datetime import datetime, timedelta
import json
import random

from fastapi.encoders import jsonable_encoder
from fastapi_sqlalchemy import db
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from app.core.config import settings
from app.models import Staff
from app.schemas.sche_staff import StaffCreateUpdateRequest
from tests.api import APITestCase
from tests.faker import fake
from app.core import error_code, message


class TestCreateUpdateStaffAPI(APITestCase):
    ISSUE_KEY = "O2OSTAFF-293"

    def common_request_create_staff(self, data={}):
        if not data.get('company_id'):
            company = fake.company_provider()
        company_id = data.get('company_id') if data.get(
            'company_id') else company.id
        if not data.get('department_id'):
            deparment = fake.department(
                {'company_id': company_id, 'is_active': True})
        department_id = data.get('department_id') if data.get(
            'department_id') else deparment.id
        if not data.get('role_title_id'):
            role_title = fake.role_title_provider(
                {'company_id': company_id, 'department_id': department_id, 'is_active': True})
        role_title_id = data.get('role_title_id') if data.get(
            'role_title_id') else role_title.id

        if not data.get('teams'):
            pass
        email = fake.email()
        staff = {
            'full_name': data.get('full_name') or fake.name(),
            'staff_code': data.get('staff_code') or fake.ean8(),
            'date_of_birth': data.get('date_of_birth') or fake.date(),
            'email_personal': data.get('email_personal') or fake.email(),
            'email': data.get('email') or email,
            'phone_number': data.get('phone_number') or fake.phone_number(),
            'manager_id': data.get('manager_id') if data.get(
                'manager_id') else None,
            'companies': [{'id': company_id, 'email': email}],
            'date_onboard': data.get('date_onboard') or (
                datetime.now() - timedelta(days=random.randint(99, 2000))).date(),
            'bank_name': data.get('bank_name') or random.choice(
                ['Vietcombank', 'MB Bank', 'Vietinbank', 'Bidv']),
            'branch_bank_name': data.get('branch_bank_name') or fake.city(),
            'account_number': data.get('account_number') or fake.bban(),
            'address_detail': data.get('address_detail') or fake.address(),
            'identity_card': data.get('identity_card') or random.randint(
                100000000, 999999999),
            'contract_type': data.get(
                'contract_type') or StaffContractType.OFFICIAL.value,
            'is_active': data.get('is_active') if data.get(
                'is_active') is not None else True,
            'department': {
                'department_id': department_id,
                'role_title_id': role_title_id,
                'is_active': True
            },
            'teams': data.get('teams') if data.get('teams') else None
        }
        return staff

    def test_000_response(self, client: TestClient):
        """
            Test api POST Create Staff response code 000
            Step by step:
            - Tạo company trong DB
            - Tạo department trong DB
            - Tạo role-title trong DB
            - Tạo team trong DB
            - Gọi POST Create Staff với đầu vào chuẩn
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        staff = self.common_request_create_staff()
        resp = client.post(
            f"{settings.BASE_API_PREFIX}/staffs", json=jsonable_encoder(staff))
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['id'] > 0

    def test_000_respose_with_manager_id(self, client: TestClient):
        """
            Test api POST Create Staff response code 000
            Step by step:
            - Tạo company trong DB
            - Tạo department trong DB
            - Tạo role-title trong DB
            - Tạo team trong DB
            - Tạo mới manager trong DB
            - Gọi POST Create Staff với đầu vào chuẩn
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        department = fake.department(
            {'company_id': company.id, 'is_active': True})
        role_title = fake.role_title_provider(
            {'company_id': company.id, 'department_id': department.id,  'is_active': True})
        team = fake.team({'company_id': company.id})
        manager = fake.staff_provider(
            {'company_id': company.id, 'is_active': True})
        email = fake.email()
        staff = StaffCreateUpdateRequest(
            full_name=fake.name(),
            staff_code=fake.unique.job(),
            email=email,
            phone_number='0974485006',
            companies=[{'id': company.id, 'email': email}],
            is_active=True,
            manager_id=manager.id,
            department={
                'department_id': department.id,
                'role_title_id': role_title.id,
                'is_active': True
            },
            teams=[{
                'team_id': team.id,
                'is_active': True
            }]
        )
        resp = client.post(
            f"{settings.BASE_API_PREFIX}/staffs", json=jsonable_encoder(staff))
        data = resp.json()
        print(data)
        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['id'] > 0

    def test_000_response_update_with_parent_id_active(self, client: TestClient):
        """
            Test api POST Update Staff response code 000
            Step by step:
            - Tạo company trong DB
            - Tạo staff1, staff2 trong DB
            - Tạo staff là con của staff1 trong DB
            - Gọi POST Update Staff với đầu vào bao gồm manager_id = department2
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        staff_parent1 = fake.staff_provider(
            {'company_id': company.id, 'is_active': True})
        staff_parent2 = fake.staff_provider(
            {'company_id': company.id, 'is_active': True})
        staff = fake.staff_provider(
            {'company_id': company.id, 'manager_id': staff_parent1.id})
        update_staff = {
            "id": staff.id,
            "manager_id": staff_parent2.id
        }
        resp = client.post(
            f"{settings.BASE_API_PREFIX}/staffs", json=jsonable_encoder(update_staff))
        data = resp.json()
        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['id'] > 0

    def test_000_mutiple_team_active(self, client: TestClient):
        """
            Test api POST Create Staff response code 000
            Step by step:
            - Tạo company trong DB
            - Gọi POST Create Staff với đầu vào nhiều team được active
            - Đầu ra mong muốn:
                . status code: 400
                . code: 000
        """
        company = fake.company_provider()
        team_1 = fake.team({"company_id": company.id})
        team_2 = fake.team({"company_id": company.id})
        team = [{'team_id': team_1.id}, {'team_id': team_2.id}]
        staff = self.common_request_create_staff(
            {"company_id": company.id, 'teams': team})
        resp = client.post(
            f"{settings.BASE_API_PREFIX}/staffs", json=jsonable_encoder(staff))
        data = resp.json()
        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['id'] > 0

    def test_001_field_requied(self, client: TestClient):
        """
            Test api POST Create Staff response code 001
            Step by step:
            - Tạo company trong DB
            - Gọi POST Create Staff với đầu vào thiếu một trường như full_name
            - Đầu ra mong muốn:
                . status code: 400
                . code: 001
        """
        staff = self.common_request_create_staff()
        del staff['full_name']
        resp = client.post(
            f"{settings.BASE_API_PREFIX}/staffs", json=jsonable_encoder(staff))
        data = resp.json()
        assert resp.status_code == 400
        assert data.get('code') == '001'
        assert data.get(
            'message') == message.MESSAGE_001_REQUIRED_FIELD_NOT_NULL

    def test_091_create_with_department_inactive(self, client: TestClient):
        """
            Test api POST Create Staff response code 001
            Step by step:
            - Tạo company trong DB
            - Gọi POST Create Staff với đầu vào department chưa được active
            - Đầu ra mong muốn:
                . status code: 400
                . code: 001
        """
        company = fake.company_provider()
        department = fake.department(
            {'company_id': company.id, 'is_active': False})
        staff = self.common_request_create_staff(
            {'company_id': company.id, 'department_id': department.id})
        resp = client.post(
            f"{settings.BASE_API_PREFIX}/staffs", json=jsonable_encoder(staff))
        data = resp.json()
        assert resp.status_code == 400
        assert data.get('code') == '091'
        assert data.get(
            'message') == message.MESSAGE_091_DEPARTMENT_ID_NOT_EXISTS

    def test_091_id_department_not_found(self, client: TestClient):
        """
            Test api POST Create Staff response code 091
            Step by step:
            - Tạo company trong DB
            - Gọi POST Create Staff với đầu đẩy đủ nhưng Department id là ngoại lệ
            - Đầu ra mong muốn:
                . status code: 400
                . code: 001
        """
        company = fake.company_provider()
        role_title = fake.role_title_provider({'company_id': company.id})
        staff = self.common_request_create_staff(
            {'department_id': 1, 'role_title_id': role_title.id})
        resp = client.post(
            f"{settings.BASE_API_PREFIX}/staffs", json=jsonable_encoder(staff))
        data = resp.json()
        assert resp.status_code == 400
        assert data.get('code') == '091'
        assert data.get(
            'message') == message.MESSAGE_091_DEPARTMENT_ID_NOT_EXISTS

    def test_097_department_and_staff_not_belong_same_company(self, client: TestClient):
        """
            Test api POST Create Staff response code 091
            Step by step:
            - Tạo company trong DB
            - Gọi POST Create Staff với đầu đẩy đủ nhưng nhân viên và phòng ban không cùng công ty
            - Đầu ra mong muốn:
                . status code: 400
                . code: 001
        # """
        company = fake.company_provider()
        company_other = fake.company_provider()
        department = fake.department(
            {'company_id': company_other.id, 'is_active': True})
        staff = self.common_request_create_staff(
            {'company_id': company.id, 'department_id': department.id})
        resp = client.post(
            f"{settings.BASE_API_PREFIX}/staffs", json=jsonable_encoder(staff))
        data = resp.json()
        assert resp.status_code == 400
        assert data.get('code') == '097'
        assert data.get(
            'message') == message.MESSAGE_097_STAFF_AND_DEPARTMENT_NOT_SAME_COMPANY

    def test_098_role_title_not_belong_department(self, client: TestClient):
        """
            Test api POST Create Staff response code 098
            Step by step:
            - Tạo company trong DB
            - Gọi POST Create Staff với đầu đẩy đủ Role_title không thuộc phòng ban
            - Đầu ra mong muốn:
                . status code: 400
                . code: 001
        """
        company = fake.company_provider()
        department = fake.department(
            {'company_id': company.id, 'is_active': True})
        department_other = fake.department(
            {'company_id': company.id, 'is_active': True})
        role_title = fake.role_title_provider(
            {'company_id': company.id, 'department_id': department_other.id, 'is_active': True})
        staff = self.common_request_create_staff(
            {'company_id': company.id, 'department_id': department.id, 'role_title_id': role_title.id})
        resp = client.post(
            f"{settings.BASE_API_PREFIX}/staffs", json=jsonable_encoder(staff))
        data = resp.json()
        assert resp.status_code == 400
        assert data.get('code') == '098'
        assert data.get(
            'message') == message.MESSAGE_098_ROLE_TITLE_NOT_BELONG_TO_DEPARTMENT

    def test_101_role_title_lock(self, client: TestClient):
        """
            Test api POST Create Staff response code 101
            Step by step:
            - Tạo company trong DB
            - Gọi POST Create Staff với đầu đẩy đủ Role_title không thuộc phòng ban
            - Đầu ra mong muốn:
                . status code: 400
                . code: 101
        """

    def test_122_email_exists(self, client: TestClient):
        """
            Test api POST Create Staff response code 122
            Step by step:
            - Tạo company trong DB
            - Gọi POST Create Staff với đầu đẩy đủ Role_title không thuộc phòng ban
            - Đầu ra mong muốn:
                . status code: 400
                . code: 122
        """
        email = fake.email()
        company = fake.company_provider()
        staff_exists = fake.staff_provider(
            {'company_id': company.id, 'email': email})
        staff = self.common_request_create_staff({'email': email})
        resp = client.post(
            f"{settings.BASE_API_PREFIX}/staffs", json=jsonable_encoder(staff))
        data = resp.json()
        assert resp.status_code == 400
        assert data.get('code') == '122'
        assert data.get(
            'message') == message.MESSAGE_122_EMAIL_ALREADY_EXISTS

    def test_124_email_invalid(self, client: TestClient):
        """
            Test api POST Create Staff response code 124
            Step by step:
            - Tạo company trong DB
            - Gọi POST Create Staff với đầu đẩy đủ nhưng email nhân viên chưa đúng định dạng
            - Đầu ra mong muốn:
                . status code: 400
                . code: 124
        """
        # chưa có
        return True

    def test_126_email_staff_exists(self, client: TestClient):
        """
            Test api POST Create Staff response code 091
            Step by step:
            - Tạo company trong DB
            - Gọi POST Create Staff với đầu đẩy đủ nhưng email không trùng nhau
            - Đầu ra mong muốn:
                . status code: 400
                . code: 001
        """
        staff = self.common_request_create_staff({'email': 'ducanh@gmail.com'})
        resp = client.post(
            f"{settings.BASE_API_PREFIX}/staffs", json=jsonable_encoder(staff))
        data = resp.json()
        assert resp.status_code == 400
        assert data.get('code') == '126'
        assert data.get(
            'message') == message.MESSAGE_126_EMAIL_COMPANY_INVALID

    def test_128_identity_card_invalid(self, client: TestClient):
        """
            Test api POST Create Staff response code 098
            Step by step:
            - Tạo company trong DB
            - Gọi POST Create Staff với đầu đẩy đủ nhưng số chứng minh thư không hợp lệ
            - Đầu ra mong muốn:
                . status code: 400
                . code: 001
        """
        staff = self.common_request_create_staff({'identity_card': '111'})
        resp = client.post(
            f"{settings.BASE_API_PREFIX}/staffs", json=jsonable_encoder(staff))
        data = resp.json()
        assert resp.status_code == 400
        assert data.get('code') == '128'
        assert data.get(
            'message') == message.MESSAGE_128_IDENTITY_CARD

    def test_129_manager_not_belong_company_of_staff(self, client: TestClient):
        """
            Test api POST Create Staff response code 129
            Step by step:
            - Tạo company trong DB
            - Gọi POST Create Staff với đầu đẩy đủ quản lý không thuộc công ty nhân viên
            - Đầu ra mong muốn:
                . status code: 400
                . code: 129
        """
        company_other = fake.company_provider()
        manager = fake.staff_provider(
            {'company_id': company_other.id, 'is_active': True})
        company = fake.company_provider()
        staff = self.common_request_create_staff(
            {'company_id': company.id, 'manager_id': manager.id})
        resp = client.post(
            f"{settings.BASE_API_PREFIX}/staffs", json=jsonable_encoder(staff))
        data = resp.json()
        assert resp.status_code == 400
        assert data.get('code') == '129'
        assert data.get(
            'message') == message.MESSAGE_129_MANAGER_ID_INVALID

    def test_130_create_with_manager_id_inactive(self, client: TestClient):
        """
            Test api POST Create Staff response code 130
            Step by step:
            - Tạo company trong DB
            - Gọi POST Create Staff với đầu đẩy đủ quản lý chưa được active
            - Đầu ra mong muốn:
                . status code: 400
                . code: 130
        """
        company = fake.company_provider()
        manager = fake.staff_provider(
            {'company_id': company.id, 'is_active': False})
        staff = self.common_request_create_staff(
            {'company_id': company.id, 'manager_id': manager.id})
        resp = client.post(
            f"{settings.BASE_API_PREFIX}/staffs", json=jsonable_encoder(staff))
        data = resp.json()
        assert resp.status_code == 400
        assert data.get('code') == '130'
        assert data.get(
            'message') == message.MESSAGE_130_MANAGER_NOT_FOUND

    def test_130_manager_id_not_found(self, client: TestClient):
        """
            Test api POST Create Staff response code 130
            Step by step:
            - Tạo company trong DB
            - Gọi POST Create Staff với đầu đẩy đủ quản lý không tồn tại
            - Đầu ra mong muốn:
                . status code: 400
                . code: 130
        """
        company = fake.company_provider()
        staff = self.common_request_create_staff(
            {'company_id': company.id, 'manager_id': -1})
        resp = client.post(
            f"{settings.BASE_API_PREFIX}/staffs", json=jsonable_encoder(staff))
        data = resp.json()
        assert resp.status_code == 400
        assert data.get('code') == '130'
        assert data.get(
            'message') == message.MESSAGE_130_MANAGER_NOT_FOUND

    def test_061_id_company_not_found(self, client: TestClient):
        """
            Test api POST Create Staff response code 061
            Step by step:
            - Tạo company trong DB
            - Gọi POST Create Staff với đầu đẩy đủ quản lý không tồn tại
            - Đầu ra mong muốn:
                . status code: 400
                . code: 061
        """
        staff = self.common_request_create_staff()
        staff["companies"][0]["id"] = 0
        resp = client.post(
            f"{settings.BASE_API_PREFIX}/staffs", json=jsonable_encoder(staff))
        data = resp.json()
        assert resp.status_code == 400
        assert data.get('code') == '061'
        assert data.get(
            'message') == message.MESSAGE_061_COMPANY_NOT_FOUND

    def test_131_date_invalid(self, client: TestClient):
        """
            Test api POST Create Staff response code 061
            Step by step:
            - Tạo company trong DB
            - Gọi POST Create Staff với đầu đẩy đủ nhưng định dạng ngày sinh bị lỗi
            - Đầu ra mong muốn:
                . status code: 400
                . code: 061
        """

    def test_132_phone_number_invalid(self, client: TestClient):
        """
            Test api POST Create Staff response code 061
            Step by step:
            - Tạo company trong DB
            - Gọi POST Create Staff với đầu đẩy đủ số điện thoại không đúng định dạng
            - Đầu ra mong muốn:
                . status code: 400
                . code: 061
        """
        staff = self.common_request_create_staff()
        staff["phone_number"] = '00'
        resp = client.post(
            f"{settings.BASE_API_PREFIX}/staffs", json=jsonable_encoder(staff))
        data = resp.json()
        assert resp.status_code == 400
        assert data.get('code') == '132'
        assert data.get(
            'message') == message.MESSAGE_132_PHONE_NUMBER_INVALID

    def test_133_agreement_invalid(self, client: TestClient):
        """
            Test api POST Create Staff response code 061
            Step by step:
            - Tạo company trong DB
            - Gọi POST Create Staff với đầu đẩy đủ loại hợp động không hợp lệ
            - Đầu ra mong muốn:
                . status code: 400
                . code: 061
        """

    def test_135_staff_code_duplicate(self, client: TestClient):
        """
            Test api POST Create Staff response code 135
            Step by step:
            - Tạo company trong DB
            - Gọi POST Create Staff với đầu đẩy đủ mã nhân viên trùng nhau
            - Đầu ra mong muốn:
                . status code: 400
                . code: 135
        """
        company = fake.company_provider()
        staff_exists = fake.staff_provider({'company_id': company.id})
        staff = self.common_request_create_staff(
            {'staff_code': staff_exists.staff_code})
        resp = client.post(
            f"{settings.BASE_API_PREFIX}/staffs", json=jsonable_encoder(staff))
        data = resp.json()
        assert resp.status_code == 400
        assert data.get('code') == '135'
        assert data.get(
            'message') == message.MESSAGE_135_STAFF_CODE_DUPLICATE

    def test_161_team_id_inactive(self, client: TestClient):
        """
            Test api POST Create Staff response code 161
            Step by step:
            - Tạo company trong DB
            - Gọi POST Create Staff với đầu đẩy đủ team id chưa được active
            - Đầu ra mong muốn:
                . status code: 400
                . code: 161
        """
        company = fake.company_provider()
        team = fake.team({'company_id': company.id, 'is_active': False})
        staff = self.common_request_create_staff({'company_id': company.id})
        staff["teams"] = [
            {
                'team_id': team.id
            }
        ]
        resp = client.post(
            f"{settings.BASE_API_PREFIX}/staffs", json=jsonable_encoder(staff))
        data = resp.json()
        assert resp.status_code == 400
        assert data.get('code') == '161'
        assert data.get(
            'message') == message.MESSAGE_161_TEAM_ID_NOT_FOUND

    def test_161_mutiple_team_but_have_team_inactive(self, client: TestClient):
        pass

    def test_161_team_id_not_found(self, client: TestClient):
        """
            Test api POST Create Staff response code 161
            Step by step:
            - Tạo company trong DB
            - Gọi POST Create Staff với đầu đẩy đủ team id không tồn tại
            - Đầu ra mong muốn:
                . status code: 400
                . code: 161
        """
        staff = self.common_request_create_staff()
        staff["teams"] = [
            {
                'team_id': 0
            }
        ]
        resp = client.post(
            f"{settings.BASE_API_PREFIX}/staffs", json=jsonable_encoder(staff))
        data = resp.json()
        assert resp.status_code == 400
        assert data.get('code') == '161'
        assert data.get(
            'message') == message.MESSAGE_161_TEAM_ID_NOT_FOUND

    def test_162_team_and_staff_not_belong_company(self, client: TestClient):
        """
            Test api POST Create Staff response code 162
            Step by step:
            - Tạo company trong DB
            - Gọi POST Create Staff với đầu đẩy đủ team id không tồn tại
            - Đầu ra mong muốn:
                . status code: 400
                . code: 162
        """
        company_other = fake.company_provider()
        company = fake.company_provider()
        team = fake.team({"company_id": company_other.id})
        staff = self.common_request_create_staff({"company_id": company.id})
        staff["teams"] = [
            {
                'team_id': team.id
            }
        ]
        resp = client.post(
            f"{settings.BASE_API_PREFIX}/staffs", json=jsonable_encoder(staff))
        data = resp.json()
        assert resp.status_code == 400
        assert data.get('code') == '162'
        assert data.get(
            'message') == message.MESSAGE_162_STAFF_AND_TEAM_NOT_BELONG_SAME_COMPANY

    def test_191_role_title_not_found(self, client: TestClient):
        """
            Test api POST Create Staff response code 191
            Step by step:
            - Tạo company trong DB
            - Gọi POST Create Staff với đầu đẩy đủ team id không tồn tại
            - Đầu ra mong muốn:
                . status code: 400
                . code: 191
        """
        staff = self.common_request_create_staff()
        staff["department"]["role_title_id"] = 0
        resp = client.post(
            f"{settings.BASE_API_PREFIX}/staffs", json=jsonable_encoder(staff))
        data = resp.json()
        assert resp.status_code == 400
        assert data.get('code') == '191'
        assert data.get(
            'message') == message.MESSAGE_191_ROLE_ID_DOES_NOT_EXITS
