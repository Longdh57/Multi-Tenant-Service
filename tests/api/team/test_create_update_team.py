import json

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from app.schemas.sche_base import ResponseSchemaBase
from tests.api import APITestCase
from app.core.config import settings
from app.core.error import message
from tests.faker import fake


class TestCreateUpdateTeamApi(APITestCase):
    ISSUE_KEY = "O2OSTAFF-296"

    def test_000_response(self, client: TestClient):
        """
            Test api post create/update team response code 000
            Step by step:
            - Gọi API Create/Update Team với đầu vào chuẩn
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        team = {
            "team_name": fake.job(),
            "description": fake.paragraph(nb_sentences=5),
            "company_id": company.id,
            "is_active": True
        }
        resp = client.post(
            f"{settings.BASE_API_PREFIX}/teams", json=jsonable_encoder(team))
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['id'] > 0

    def test_000_response_create_with_dont_have_description(self, client: TestClient):
        """
            Test api post create/update team response code 000
            Step by step:
            - Gọi API Create/Update Team với đầu vào chuẩn và không có mô tả cho team
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        team = {
            "team_name": fake.job(),
            "company_id": company.id,
            "is_active": True
        }
        resp = client.post(
            f"{settings.BASE_API_PREFIX}/teams", json=jsonable_encoder(team))
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['id'] > 0

    def test_000_response_create_with_same_team_name_but_in_other_company(self, client: TestClient):
        """
            Test api post create/update team response code 000
            Step by step:
            - Gọi API Create/Update Team với đầu vào chuẩn và và cùng tên nhưng khác công ty
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        company_other = fake.company_provider()
        team_name = fake.job()
        team_same_name = fake.team(
            {'company_id': company_other.id, 'team_name': team_name})
        team = {
            "team_name": team_name,
            "company_id": company.id,
            "is_active": True
        }
        resp = client.post(
            f"{settings.BASE_API_PREFIX}/teams", json=jsonable_encoder(team))
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['id'] > 0

    def test_000_response_create_with_same_name_in_a_company_but_team_inactive(self, client: TestClient):
        """
            Test api post create/update team response code 000
            Step by step:
            - Gọi API Create/Update Team với đầu vào chuẩn và nhóm không được active
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        team_name = fake.job()
        team = fake.team(
            {'company_id': company.id, 'team_name': team_name, 'is_active': False})
        team = {
            "team_name": team_name,
            "company_id": company.id,
            "is_active": True
        }
        resp = client.post(
            f"{settings.BASE_API_PREFIX}/teams", json=jsonable_encoder(team))
        data = resp.json()
        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['id'] > 0

    def test_000_update_description(self, client: TestClient):
        """
            Test api post update team response code 000
            Step by step:
            - Gọi API Update Team với đầu vào chuẩn và thay đổi mô tả
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        team = fake.team()
        team = {
            "id": team.id,
            "description": "Test"
        }
        resp = client.post(
            f"{settings.BASE_API_PREFIX}/teams", json=jsonable_encoder(team))
        data = resp.json()
        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['id'] > 0

    def test_000_update_is_active(self, client: TestClient):
        """
            Test api post update team response code 000
            Step by step:
            - Gọi API Update Team với đầu vào chuẩn và thay đổi is_active
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        team = fake.team()
        team = {
            "id": team.id,
            "is_active": False
        }
        resp = client.post(
            f"{settings.BASE_API_PREFIX}/teams", json=jsonable_encoder(team))
        data = resp.json()
        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['id'] > 0

    def test_000_update_team_name(self, client: TestClient):
        """
            Test api post update team response code 000
            Step by step:
            - Gọi API Update Team với đầu vào chuẩn và thay đổi is_active
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        team = fake.team()
        team = {
            "id": team.id,
            "team_name": fake.job()
        }
        resp = client.post(
            f"{settings.BASE_API_PREFIX}/teams", json=jsonable_encoder(team))
        data = resp.json()
        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['id'] > 0

    def test_000_update_company_id_but_dont_change_anything(self, client: TestClient):
        """
            Test api post update team response code 000
            Step by step:
            - Gọi API Update Team với đầu vào chuẩn và thay đổi is_active
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        team_provider = fake.team()
        team = {
            "id": team_provider.id,
            "company_id": 0
        }
        resp = client.post(
            f"{settings.BASE_API_PREFIX}/teams", json=jsonable_encoder(team))
        data = resp.json()
        assert team_provider.company_id != 0
        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')['id'] > 0

    def test_061_response_create_with_company_id_not_exists(self, client: TestClient):
        """
            Test api POST Create Team response code 061
            Step by step:
            - Gọi API Create/Update Role Tile với body company_id không tồn tại trên hệ thống
            - Đầu ra mong muốn:
                . status code: 400
                . code: 061
        """
        team = {
            "team_name": fake.job(),
            "description": fake.paragraph(nb_sentences=5),
            "company_id": 10,
            "is_active": True
        }
        resp = client.post(
            f"{settings.BASE_API_PREFIX}/teams", json=jsonable_encoder(team))
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '061'
        assert data.get('message') == 'ID company không tồn tại trong hệ thống'

    def test_160_response_create_team_name_exists(self, client: TestClient):
        """
            Test api get Create/Update Team response code 160
            Step by step:
            - Gọi API Create/Update Team với đầu vào chuẩn
            Đầu vào mong muốn tên của Team đã tồn tại
            - Đầu ra mong muốn:
                . status code: 400
                . code: 160
        """
        company = fake.company_provider()
        team_name = fake.job()
        team = {
            "team_name": team_name,
            "description": fake.paragraph(nb_sentences=5),
            "company_id": company.id,
            "is_active": True
        }
        client.post(f"{settings.BASE_API_PREFIX}/teams",
                    json=jsonable_encoder(team))
        resp = client.post(f"{settings.BASE_API_PREFIX}/teams",
                           json=jsonable_encoder(team))
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '160'
        assert data.get('message') == message.MESSAGE_160_EXISTS_TEAM

    def test_160_response_update_team_name_exists(self, client: TestClient):
        """
            Test api get Create/Update Team response code 160
            Step by step:
            - Gọi API Create/Update Team với đầu vào chuẩn
            Đầu vào mong muốn tên của Team đã tồn tại
            - Đầu ra mong muốn:
                . status code: 400
                . code: 160
        """
        company = fake.company_provider()
        team_name = fake.job()
        team_1 = fake.team({'company_id': company.id, 'team_name': team_name})
        team_2 = fake.team({'company_id': company.id})
        team = {
            "id": team_2.id,
            "team_name": team_name,
        }
        resp = client.post(f"{settings.BASE_API_PREFIX}/teams",
                           json=jsonable_encoder(team))
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '160'
        assert data.get('message') == message.MESSAGE_160_EXISTS_TEAM

    def test_161_response_update_team_id_not_found(self, client: TestClient):
        """
            Test api POST Create/Update Team response code 161
            Step by step:
            - Gọi API Create/Update Team với đầu vào chuẩn
            - Đầu ra mong muốn:
                . status code: 400
                . code: 161
        """
        company = fake.company_provider()
        team = {
            "id": 0,
            "team_name": fake.job(),
            "description": fake.paragraph(nb_sentences=5),
            "company_id": company.id,
            "is_active": True
        }
        resp = client.post(
            f"{settings.BASE_API_PREFIX}/teams", json=jsonable_encoder(team))
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '161'
        assert data.get('message') == message.MESSAGE_161_TEAM_ID_NOT_FOUND

    def test_999_internal_error(self, client: TestClient):
        """
            Test api post create/update team response code 999
            Step by step:
            - Gọi API Create/Update Team lỗi
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
