from app.models.model_staff_team import StaffTeam
import json
import random
from fastapi_sqlalchemy import db

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from app.core.config import settings
from app.schemas.sche_base import ResponseSchemaBase
from tests.api import APITestCase
from tests.faker import fake
from app.core import error_code, message


class TestGetTeamDetailApi(APITestCase):
    ISSUE_KEY = "O2OSTAFF-295"

    def test_000_success(self, client: TestClient):
        """
            Test api get Team detail to team response code 000
            Step by step:
            - Gọi API Team Detail với đầu vào chuẩn
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        team = fake.team({'company_id': company.id})
        resp = client.get(f"{settings.BASE_API_PREFIX}/teams/{team.id}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['team_name'] == team.team_name

    def test_000_success_get_team_with_multi_staffs(self, client: TestClient):
        company = fake.company_provider()
        team = fake.team({'company_id': company.id})

        number_staffs = random.randint(2, 10)
        staffs = [fake.staff_provider(
            {'company_id': company.id, 'is_active': True}) for _ in range(number_staffs)]

        team_staff_mappings = [{
            'team_id': team.id,
            'staff_id': staff.id,
            'is_active': True
        } for staff in staffs]
        with db():
            db.session.bulk_insert_mappings(StaffTeam, team_staff_mappings)
            db.session.commit()
        resp = client.get(f"{settings.BASE_API_PREFIX}/teams/{team.id}")
        data = resp.json()
        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['count_staff'] == number_staffs


    def test_161_response_id_not_found(self, client: TestClient):
        """
            Test api get Team detail to team response code 000
            Step by step:
            - Gọi API Team Detail với đầu vào chuẩn
            - Đầu ra mong muốn:
                . status code: 200
                . code: 161
        """
        team = fake.team()
        resp = client.get(f"{settings.BASE_API_PREFIX}/teams/10000000")
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '161'
        assert data.get('message') == message.MESSAGE_161_TEAM_ID_NOT_FOUND

    def test_999_internal_error(self, client: TestClient):
        """
            Test api get Team detail response code 999
            Step by step:
            - Gọi API Team Detail lỗi
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
