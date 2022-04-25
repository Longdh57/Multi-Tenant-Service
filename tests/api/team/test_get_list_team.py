import json

from fastapi.encoders import jsonable_encoder
from sqlalchemy.sql.expression import true
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from app.core.config import settings
from app.schemas.sche_base import ResponseSchemaBase
from tests.api import APITestCase
from tests.faker import fake
from app.core import error_code, message


class TestGetListTeamApi(APITestCase):
    ISSUE_KEY = "O2OSTAFF-294"

    def test_000_response(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Gọi API Team List với đầu vào chuẩn
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        fake.teams(company=company)

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/teams?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') <= 100

    def test_000_response_search_team_name_with_keyword_match_all(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Gọi API Team List với đầu vào chuẩn search name match all
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        keyword = 'Team với keyword match all'
        fake.team({'company_id': company.id,
                  'team_name': keyword, 'is_active': True})
        fake.team({'company_id': company.id,
                  'team_name': keyword, 'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/teams?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&search={keyword}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 2

    def test_000_response_search_team_name_with_keyword_like(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Tạo 1 Team có name = "team với like"
            - Tạo 1 Team có name = "Test với keyword like"
            - Tạo 1 Team có name = "Test keyword like"
            - Gọi API team List với đầu vào chuẩn type = list, team_name = "với"
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 2
        """
        company = fake.company_provider()
        fake.team({'company_id': company.id,
                   'team_name': 'team với like', 'is_active': True, 'description': ''})
        fake.team({'company_id': company.id,
                   'team_name': 'Test với keyword like', 'is_active': True, 'description': ''})
        fake.team({'company_id': company.id,
                   'team_name': 'Test keyword like', 'description': '', 'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/teams?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&search={'với'}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 2

    def test_000_response_search_team_name_with_not_match_any_team(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Tạo 1 Team có name = "team với like"
            - Tạo 1 Team có name = "Test với keyword like"
            - Tạo 1 Team có name = "Test keyword like"
            - Gọi API team List với đầu vào chuẩn type = list, team_name = "abc"
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 0
        """
        company = fake.company_provider()
        fake.team({'company_id': company.id,
                   'team_name': 'team với like', 'is_active': True, 'description': ''})
        fake.team({'company_id': company.id,
                   'team_name': 'Test với keyword like', 'is_active': True, 'description': ''})
        fake.team({'company_id': company.id,
                   'team_name': 'Test keyword like', 'description': '', 'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/teams?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&search={'abc'}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 0

    def test_000_response_search_team_name_with_keyword_lowcase(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Tạo 1 Team có name = "team với like"
            - Tạo 1 Team có name = "Test với keyword like"
            - Tạo 1 Team có name = "Test keyword like"
            - Gọi API team List với đầu vào chuẩn type = list, team_name = "với"
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 2
        """
        company = fake.company_provider()
        fake.team({'company_id': company.id,
                   'team_name': 'team với like', 'is_active': True, 'description': ''})
        fake.team({'company_id': company.id,
                   'team_name': 'Test với keyword like', 'is_active': True, 'description': ''})
        fake.team({'company_id': company.id,
                   'team_name': 'Test keyword like', 'description': '', 'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/teams?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&search={'với'}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 2

    def test_000_response_search_team_name_with_keyword_uppercase(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Tạo 1 Team có name = "team với like"
            - Tạo 1 Team có name = "Test với keyword like"
            - Tạo 1 Team có name = "Test keyword like"
            - Gọi API team List với đầu vào chuẩn type = list, team_name = "với"
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 2
        """
        company = fake.company_provider()
        fake.team({'company_id': company.id,
                   'team_name': 'team với like', 'is_active': True, 'description': ''})
        fake.team({'company_id': company.id,
                   'team_name': 'Test với keyword like', 'is_active': True, 'description': ''})
        fake.team({'company_id': company.id,
                   'team_name': 'Test keyword like', 'description': '', 'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/teams?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&search={'VỚI'}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 2

    def test_000_response_search_team_name_with_keyword_accented_vietnamese(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Tạo 1 Team có name = "team với like"
            - Tạo 1 Team có name = "Test với keyword like"
            - Tạo 1 Team có name = "Test keyword like"
            - Gọi API team List với đầu vào chuẩn type = list, team_name = "với"
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 2
        """
        company = fake.company_provider()
        fake.team({'company_id': company.id,
                   'team_name': 'team với like', 'is_active': True, 'description': ''})
        fake.team({'company_id': company.id,
                   'team_name': 'Test với keyword like', 'is_active': True, 'description': ''})
        fake.team({'company_id': company.id,
                   'team_name': 'Test keyword like', 'description': '', 'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/teams?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&search={'VỚI'}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 2

    def test_000_response_check_staff_count_of_team_with_count_staff(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Tạo 1 Team có name = "team với like"
            - Tạo 1 Team có name = "Test với keyword like"
            - Tạo 1 Team có name = "Test keyword like"
            - Gọi API team List với đầu vào chuẩn type = list, team_name = "với"
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 2
        """
        company = fake.company_provider()
        team = fake.team({'company_id': company.id,
                          'team_name': 'team với like', 'is_active': True, 'description': ''})
        fake.add_staff_to_team(company, team)

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/teams?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&search={'VỚI'}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('data')[0].get('count_staff') == 1
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 1

    def test_000_response_search_team_description_with_keyword_match_all(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Gọi API Team List với đầu vào chuẩn search description match all
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
        """
        company = fake.company_provider()
        keyword = 'Team với keyword match all'
        fake.team({'company_id': company.id,
                  'team_name': '1', 'is_active': True, 'description': keyword})
        fake.team({'company_id': company.id,
                  'team_name': '2', 'is_active': True, 'description': keyword})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/teams?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&search={keyword}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 2

    def test_000_response_search_team_description_with_keyword_like(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Tạo 1 Team có description = "team với like"
            - Tạo 1 Team có description = "Test với keyword like"
            - Tạo 1 Team có description = "Test keyword like"
            - Gọi API team List với đầu vào chuẩn type = list, search = "với"
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 2
        """
        company = fake.company_provider()
        fake.team({'company_id': company.id,
                   'description': 'team với like', 'is_active': True, 'team_name': '1'})
        fake.team({'company_id': company.id,
                   'description': 'Test với keyword like', 'is_active': True, 'team_name': '2'})
        fake.team({'company_id': company.id,
                   'description': 'Test keyword like', 'team_name': '3', 'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/teams?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&search={'với'}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 2

    def test_000_response_search_team_description_with_not_match_any_name_description(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Tạo 1 Team có description = "team với like"
            - Tạo 1 Team có description = "Test với keyword like"
            - Tạo 1 Team có description = "Test keyword like"
            - Gọi API team List với đầu vào chuẩn type = list, search = "với"
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 2
        """
        company = fake.company_provider()
        fake.team({'company_id': company.id,
                   'description': 'team với like', 'is_active': True, 'team_name': '1'})
        fake.team({'company_id': company.id,
                   'description': 'Test với keyword like', 'is_active': True, 'team_name': '2'})
        fake.team({'company_id': company.id,
                   'description': 'Test keyword like', 'team_name': '3', 'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/teams?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&search={'abccc'}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 0

    def test_000_response_search_team_description_with_keyword_lowcase(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Tạo 1 Team có description = "team với like"
            - Tạo 1 Team có description = "Test với keyword like"
            - Tạo 1 Team có description = "Test keyword like"
            - Gọi API team List với đầu vào chuẩn type = list, search = "với"
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 2
        """
        company = fake.company_provider()
        fake.team({'company_id': company.id,
                   'description': 'team với like', 'is_active': True, 'team_name': '1'})
        fake.team({'company_id': company.id,
                   'description': 'Test với keyword like', 'is_active': True, 'team_name': '2'})
        fake.team({'company_id': company.id,
                   'description': 'Test keyword like', 'team_name': '3', 'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/teams?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&search={'với'}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 2

    def test_000_response_search_team_description_with_keyword_accented_vietnamese(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Tạo 1 Team có description = "team với like"
            - Tạo 1 Team có description = "Test với keyword like"
            - Tạo 1 Team có description = "Test keyword like"
            - Gọi API team List với đầu vào chuẩn type = list, search = "với"
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 2
        """
        company = fake.company_provider()
        fake.team({'company_id': company.id,
                   'description': 'team với like', 'is_active': True, 'team_name': '1'})
        fake.team({'company_id': company.id,
                   'description': 'Test với keyword like', 'is_active': True, 'team_name': '2'})
        fake.team({'company_id': company.id,
                   'description': 'Test keyword like', 'team_name': '3', 'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/teams?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&search={'VỚI'}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 2

    def test_000_check_default_sort_by_order(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Gọi API team List với đầu vào chuẩn type = list, oder by id
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 2
        """
        company = fake.company_provider()
        fake.team({'company_id': company.id,
                   'description': 'team với like', 'is_active': True, 'team_name': '1'})
        fake.team({'company_id': company.id,
                   'description': 'Test với keyword like', 'is_active': True, 'team_name': '2'})
        fake.team({'company_id': company.id,
                   'description': 'Test keyword like', 'team_name': '3', 'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/teams?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&search={'VỚI'}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('data')[0]['id'] > data.get('data')[1]['id']

    def test_000_check_sort_by_name_desc(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Gọi API team List với đầu vào chuẩn type = list, oder by team_name
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 2
        """
        company = fake.company_provider()
        fake.team({'company_id': company.id,
                   'description': 'team với like', 'is_active': True, 'team_name': '1'})
        fake.team({'company_id': company.id,
                   'description': 'Test với keyword like', 'is_active': True, 'team_name': '2'})
        fake.team({'company_id': company.id,
                   'description': 'Test keyword like', 'team_name': '3', 'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/teams?page_size=10&page=1&sort_by=id&order=desc&company_id={company.id}&type=list&search={'VỚI'}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('data')[0]['team_name'] > data.get(
            'data')[1]['team_name']

    def test_000_check_sort_by_name_asc(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Gọi API team List với đầu vào chuẩn type = list, oder by team_name
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 2
        """
        company = fake.company_provider()
        fake.team({'company_id': company.id,
                   'description': 'team với like', 'is_active': True, 'team_name': '1'})
        fake.team({'company_id': company.id,
                   'description': 'Test với keyword like', 'is_active': True, 'team_name': '2'})
        fake.team({'company_id': company.id,
                   'description': 'Test keyword like', 'team_name': '3', 'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/teams?page_size=10&page=1&sort_by=id&order=asc&company_id={company.id}&type=list&search={'VỚI'}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('data')[0]['team_name'] < data.get(
            'data')[1]['team_name']

    def test_000_check_sort_by_updated_at_desc(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Gọi API team List với đầu vào chuẩn type = list, oder by update_at
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 2
        """
        company = fake.company_provider()
        fake.team({'company_id': company.id,
                   'description': 'team với like', 'is_active': True, 'team_name': '1'})
        fake.team({'company_id': company.id,
                   'description': 'Test với keyword like', 'is_active': True, 'team_name': '2'})
        fake.team({'company_id': company.id,
                   'description': 'Test keyword like', 'team_name': '3', 'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/teams?page_size=10&page=1&sort_by=updated_at&order=desc&company_id={company.id}&type=list&search={'VỚI'}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('data')[0]['updated_at'] >= data.get(
            'data')[1]['updated_at']

    def test_000_check_sort_by_updated_at_asc(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Gọi API team List với đầu vào chuẩn type = list, oder by update_at
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 2
        """
        company = fake.company_provider()
        fake.team({'company_id': company.id,
                   'description': 'team với like', 'is_active': True, 'team_name': '1'})
        fake.team({'company_id': company.id,
                   'description': 'Test với keyword like', 'is_active': True, 'team_name': '2'})
        fake.team({'company_id': company.id,
                   'description': 'Test keyword like', 'team_name': '3', 'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/teams?page_size=10&page=1&sort_by=updated_at&order=asc&company_id={company.id}&type=list&search={'VỚI'}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('data')[0]['updated_at'] <= data.get(
            'data')[1]['updated_at']

    def test_000_check_sort_by_created_at_desc(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Gọi API team List với đầu vào chuẩn type = list, oder by created_at
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 2
        """
        company = fake.company_provider()
        fake.team({'company_id': company.id,
                   'description': 'team với like', 'is_active': True, 'team_name': '1'})
        fake.team({'company_id': company.id,
                   'description': 'Test với keyword like', 'is_active': True, 'team_name': '2'})
        fake.team({'company_id': company.id,
                   'description': 'Test keyword like', 'team_name': '3', 'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/teams?page_size=10&page=1&sort_by=created_at&order=desc&company_id={company.id}&type=list&search={'VỚI'}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('data')[0]['created_at'] >= data.get(
            'data')[1]['created_at']

    def test_000_check_sort_by_create_at_asc(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Gọi API team List với đầu vào chuẩn type = list, oder by created_at
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 2
        """
        company = fake.company_provider()
        fake.team({'company_id': company.id,
                   'description': 'team với like', 'is_active': True, 'team_name': '1'})
        fake.team({'company_id': company.id,
                   'description': 'Test với keyword like', 'is_active': True, 'team_name': '2'})
        fake.team({'company_id': company.id,
                   'description': 'Test keyword like', 'team_name': '3', 'is_active': True})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/teams?page_size=10&page=1&sort_by=created_at&order=asc&company_id={company.id}&type=list&search={'VỚI'}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('data')[0]['created_at'] <= data.get(
            'data')[1]['created_at']

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
        fake.teams(company=company, total=40)

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/teams?page_size=30&page=1&company_id={company.id}")
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
            - Gọi API team List với đầu vào chuẩn type = list, 40 team, 30 page_size ở page 2
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 40
        """
        company = fake.company_provider()
        fake.teams(company=company, total=40)

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/teams?page_size=30&page=3&company_id={company.id}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 40
        assert data.get('metadata').get('page_size') == 30
        assert data.get('metadata').get('current_page') == 3

    def test_000_check_paging_40_records_page_size_30_page_equal_3(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Gọi API team List với đầu vào chuẩn type = list, 40 team, 30 page_size ở page 2
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 40
        """
        company = fake.company_provider()
        fake.teams(company=company, total=40)

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/teams?page_size=30&page=3&sort_by=created_at&order=asc&company_id={company.id}")
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
            - Gọi API team List với đầu vào chuẩn type = list, 40 team, 30 page_size ở page 2
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 40
        """
        company = fake.company_provider()
        fake.teams(company=company, total=40)

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/teams?page_size=50&page=1&sort_by=created_at&order=asc&company_id={company.id}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 40
        assert data.get('metadata').get('page_size') == 50
        assert data.get('metadata').get('current_page') == 1

    def test_000_check_paging_40_records_page_size_30_page_equal_1_sort_by_create_at_order_desc(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Gọi API team List với đầu vào chuẩn type = list, 40 team, 30 page_size ở page 2 created_at sort by desc
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 40
        """
        company = fake.company_provider()
        fake.teams(company=company, total=40)

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/teams?page_size=50&page=1&sort_by=created_at&order=desc&company_id={company.id}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 40
        assert data.get('metadata').get('page_size') == 50
        assert data.get('metadata').get('current_page') == 1
        assert data.get('data')[0]['created_at'] >= data.get(
            'data')[1]['created_at']

    def test_000_check_paging_40_records_page_size_30_page_equal_2_sort_by_create_at_order_asc(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Gọi API team List với đầu vào chuẩn type = list, 40 team, 30 page_size ở page 2 created_at sort by asc
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 40
        """
        company = fake.company_provider()
        fake.teams(company=company, total=40)

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/teams?page_size=50&page=1&sort_by=created_at&order=asc&company_id={company.id}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 40
        assert data.get('metadata').get('page_size') == 50
        assert data.get('metadata').get('current_page') == 1
        assert data.get('data')[0]['created_at'] <= data.get(
            'data')[1]['created_at']

    def test_000_have_inactive_team(self, client: TestClient):
        """
            Test api get Team List response code 000
            Step by step:
            - Gọi API team List với đầu vào chuẩn type = list, 40 team, 30 page_size ở page 2 created_at sort by asc
            - Đầu ra mong muốn:
                . status code: 200
                . code: 000
                . total_items: 40
        """
        company = fake.company_provider()
        fake.teams(company=company, total=40)
        fake.team({'company_id': company.id, 'is_active': False})

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/teams?page_size=50&page=1&sort_by=created_at&order=asc&company_id={company.id}")
        data = resp.json()

        assert resp.status_code == 200
        assert data.get('code') == '000'
        assert data.get('message') == 'Thành công'
        assert data.get('metadata') is not None
        assert data.get('metadata').get('total_items') == 40
        assert data.get('metadata').get('page_size') == 50
        assert data.get('metadata').get('current_page') == 1
        assert data.get('data')[0]['created_at'] <= data.get(
            'data')[1]['created_at']

    def test_002_response_pagesize_larger_than_0(self, client: TestClient):
        """
            Test api get Team List response code 002
            Step by step:
            - Gọi API Team List với param: page_size < 0
            - Đầu ra mong muốn:
                . status code: 400
                . code: 002
        """
        company = fake.company_provider()
        for i in range(10):
            fake.teams(company=company)

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/teams?page_size=-1&page=1&sort_by=id&order=desc&company_id={company.id}")
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '002'
        assert data.get(
            'message') == message.MESSAGE_002_PAGE_SIZE_LARGE_THAN_0

    def test_003_response_page_larger_than_0(self, client: TestClient):
        """
            Test api get Team List response code 003
            Step by step:
            - Gọi API Team List với param: page < 0
            - Đầu ra mong muốn:
                . status code: 400
                . code: 003
        """
        company = fake.company_provider()
        fake.teams(company=company)

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/teams?page_size=10&page=-1&sort_by=id&order=desc&company_id={company.id}")
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '003'
        assert data.get('message') == message.MESSAGE_003_PAGE_LARGE_THAN_0

    def test_005_response_order_invalid(self, client: TestClient):
        """
            Test api get Team List response code 005
            Step by step:
            - Gọi API team List với param: order không phải là asc|desc
            - Đầu ra mong muốn:
                . status code: 400
                . code: 005
        """
        company = fake.company_provider()
        fake.teams(company=company)

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/teams?page_size=10&page=1&sort_by=id&order=esc&company_id={company.id}&type=list")
        data = resp.json()

        assert resp.status_code == 400
        assert data.get('code') == '005'
        assert data.get('message') == message.MESSAGE_005_ORDER_VALUE_INVALID

    def test_010_sort_by_invalid_(self, client: TestClient):
        """
            Test api get Team List response code 010
            Step by step:
            - Gọi API team List với param: order không phải là asc|desc
            - Đầu ra mong muốn:
                . status code: 400
                . code: 010
        """

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
        fake.teams(company=company, total=40)

        resp = client.get(
            f"{settings.BASE_API_PREFIX}/teams?page_size=10&page=1&sort_by=id&order=desc")
        data = resp.json()
        print(resp.json())
        assert resp.status_code == 400
        assert data.get('code') == '001'

    def test_051_response_params_type_invalid(self, client: TestClient):
        """
            Test api get Team List response code 051
            Step by step:
            - Gọi API Team List với param: type khác ["tree", "list"]
            - Đầu ra mong muốn:
                . status code: 400
                . code: 051
        """
        assert True

    def test_999_internal_error(self, client: TestClient):
        """
            Test api get Team List response code 999
            Step by step:
            - Gọi API Team List lỗi
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
