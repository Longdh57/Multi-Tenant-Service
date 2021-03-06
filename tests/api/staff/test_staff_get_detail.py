from app.helpers.enums import StaffContractType
from datetime import datetime, timedelta
from app.services.srv_staff import StaffService
import json
import random

from fastapi.encoders import jsonable_encoder
from fastapi_sqlalchemy import db
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from app.core.config import settings
from app.models import Staff
from app.schemas.sche_base import ResponseSchemaBase
from app.schemas.sche_staff import StaffCreateUpdateRequest
from tests.api import APITestCase
from tests.faker import fake
from app.core import error_code, message


class TestGetDetailStaff(APITestCase):
    ISSUE_KEY = "O2OSTAFF-292"

    @staticmethod
    def common_request_create_staff(data={}, total_team=3):
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
        teams = []
        for i in range(total_team):
            team = fake.team({'company_id': company_id})
            teams.append({
                "team_id": team.id
            })
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
            'teams': data.get('teams') if data.get('teams') else teams
        }

        return staff

    def test_000_success_response(self, client: TestClient):
        """
            Test api GET Detail Staff response code 000
            Step by step:
            - T???o m???t Staff m???i trong db
            - G???i api Staff Detail v???i ?????u v??o l?? id c???a staff
            - ?????u ra mong mu???n:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        staff = fake.staff_provider(
            {'company_id': company.id, 'is_active': True})
        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs/{staff.id}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Th??nh c??ng'
        assert data.get('data')['full_name'] == staff.full_name

    def test_000_response_get_by_email(self, client: TestClient):
        """
            Test api GET Detail Staff response code 000
            Step by step:
            - T???o m???t Staff m???i trong db
            - G???i api Staff Detail v???i ?????u v??o l?? email c???a staff
            - ?????u ra mong mu???n:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        email = fake.email()
        staff = fake.staff_provider(
            {'company_id': company.id, 'is_active': True, 'email': email})
        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs/{staff.email}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Th??nh c??ng'
        assert data.get('data')['email'] == staff.email

    def test_000_response_none_manager_id(self, client: TestClient):
        """
            Test api GET Detail Staff response code 000
            Step by step:
            - T???o m???t v??i Staff m???i trong db kh??ng c?? manager_id
            - G???i api Staff Detail v???i ?????u v??o l?? id c???a staff
            - ?????u ra mong mu???n:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        email = fake.email()
        staff = fake.staff_provider(
            {'company_id': company.id, 'is_active': True, 'email': email})
        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs/{staff.id}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Th??nh c??ng'
        assert data.get('data')['manager']['id'] == None

    def test_000_response_with_staff_have_manager_id(self, client: TestClient):
        """
            Test api GET Detail Staff response code 000
            Step by step:
            - T???o m???t Staff1 m???i trong db
            - T???o m???t staff kh??c c?? manager_id l?? id c???a staff1
            - G???i api Staff Detail v???i ?????u v??o l?? id c???a staff
            - ?????u ra mong mu???n:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        email = fake.email()
        manager = fake.staff_provider({'company_id': company.id})
        staff = fake.staff_provider(
            {'company_id': company.id, 'is_active': True, 'manager_id': manager.id})
        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs/{staff.id}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Th??nh c??ng'
        assert data.get('data')['manager']['id'] == manager.id

    def test_000_response_with_staff_have_3_children(self, client: TestClient):
        """
        Test api GET Detail Staff response code 000
        Step by step:
        - T???o m???t Staff1 m???i trong db
        - T???o 3 staff kh??c c?? manager_id l?? id c???a staff1
        - G???i api Staff Detail v???i ?????u v??o l?? id c???a staff
        - ?????u ra mong mu???n:
            . status code: 200
            . code: 000
        """
        company = fake.company_provider()
        email = fake.email()
        manager = fake.staff_provider({'company_id': company.id})
        for i in range(3):
            fake.staff_provider(
                {'company_id': company.id, 'is_active': True, 'manager_id': manager.id})
        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs/{manager.id}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Th??nh c??ng'
        assert len(data.get('data')['children']) == 3

    def test_000_response_with_3_level_staff(self, client: TestClient):
        """
        Test api GET Detail Staff response code 000
        Step by step:
        - T???o m???t staff cha m???i trong db
        - T???o m???t staff con m???i trong db
        - T???o m???t staff con c???a con m???i trong db
        - G???i api Staff Detail v???i ?????u v??o l?? id c???a staff
        - ?????u ra mong mu???n:
            . status code: 200
            . code: 000
        """
        company = fake.company_provider()
        email = fake.email()
        manager = fake.staff_provider({'company_id': company.id})
        level2 = fake.staff_provider(
            {'company_id': company.id, 'is_active': True, 'manager_id': manager.id})
        level3 = fake.staff_provider(
            {'company_id': company.id, 'is_active': True, 'manager_id': level2.id})
        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs/{manager.id}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Th??nh c??ng'
        assert data.get('data')['children'][0]["id"] == level2.id
        assert data.get('data')[
            'children'][0]['children'][0]['id'] == level3.id

    def test_000_response_with_3_staff_in_multiple_team(self, client: TestClient):
        """
        Test api GET Detail Staff response code 000
        Step by step:
        - T???o m???i m???t v??i team
        - T???o m???t staff v??o nhi???u team kh??c nhau
        - G???i api Staff Detail v???i ?????u v??o l?? id c???a staff
        - ?????u ra mong mu???n:
            . status code: 200
            . code: 000
        """
        company = fake.company_provider()
        staff = self.common_request_create_staff({'company_id': company.id})
        staff_response = client.post(
            f"{settings.BASE_API_PREFIX}/staffs", json=jsonable_encoder(staff))
        data = staff_response.json()
        print(data)
        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs/{data.get('data')['id']}")
        data = resp.json()
        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Th??nh c??ng'
        assert len(data.get('data')['team']) > 1

    def test_004_field_value_invalid(self, client: TestClient):
        """
        Test api GET Detail Staff response code 004
        Step by step:
        - T???o m???t staff 
        - G???i api get staff detail nh??ng ?????u v??o kh??ng ????ng ?????nh d???ng
        - ?????u ra mong mu???n:
            . status code: 200
            . code: 004
        """
        company = fake.company_provider()
        staff = fake.staff_provider(
            {'company_id': company.id, 'is_active': True})
        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs/a")
        data = resp.json()
        assert resp.status_code == 400
        assert data.get('code') == '004'
        assert data.get('message') == message.MESSAGE_004_FIELD_VALUE_INVALID

    def test_121_email_not_found(self, client: TestClient):
        """
        Test api GET Detail Staff response code 121
        Step by step:
        - T???o m???t staff 
        - G???i api get staff detail ?????u v??o ????ng ?????nh d???ng nh??ng email kh??ng t??m th???y
        - ?????u ra mong mu???n:
            . status code: 200
            . code: 121
        """
        company = fake.company_provider()
        email = fake.email()
        staff = fake.staff_provider(
            {'company_id': company.id, 'is_active': True})
        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs/{email}")
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '121'
        assert data.get('message') == message.MESSAGE_121_EMAIL_NOT_FOUND

    def test_134_response_id_staff_not_found(self, client: TestClient):
        """
        Test api GET Detail Staff response code 134
        Step by step:
        - T???o m???t staff
        - G???i api Staff Detail v???i ?????u v??o l?? id c???a staff kh??ng t???n t???i trong h??? th???ng
        - ?????u ra mong mu???n:
            . status code: 200
            . code: 134
        """
        company = fake.company_provider()
        staff = fake.staff_provider(
            {'company_id': company.id, 'is_active': True})
        resp = client.get(
            f"{settings.BASE_API_PREFIX}/staffs/0")
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '134'
        assert data.get('message') == message.MESSAGE_134_STAFF_ID_NOT_FOUND

    def test_999_internal_error(self, client: TestClient):
        """
            Test api get Department Detail response code 999
            Step by step:
            - G???i API Department Detail l???i
            - ?????u ra mong mu???n:
                . status code: 500
                . code: 999
        """
        res = JSONResponse(
            status_code=500,
            content=jsonable_encoder(
                ResponseSchemaBase().custom_response(
                    '999', "H??? th???ng ??ang b???o tr??, qu?? kh??ch vui l??ng th??? l???i sau"
                )
            )
        )
        assert res.status_code == 500 and json.loads(res.body) == {
            "code": "999",
            "message": "H??? th???ng ??ang b???o tr??, qu?? kh??ch vui l??ng th??? l???i sau"
        }
