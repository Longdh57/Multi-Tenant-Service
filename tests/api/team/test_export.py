import json

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from app.schemas.sche_base import ResponseSchemaBase
from tests.api import APITestCase


class TestExportData(APITestCase):
    ISSUE_KEY = "O2OSTAFF-529"

    def test_export_data_staff(self):
        pass

    def test_export_data_company(self):
        pass

    def test_export_data_corporation(self):
        pass

    def test_export_data_department(self):
        pass

    def test_export_data_role_title(self):
        pass

    def test_export_data_department_staff(self):
        pass

    def test_export_data_company_staff(self):
        pass

    def test_export_data_staff_team(self):
        pass

    def test_export_data_staff_have_parent(self):
        pass

    def test_export_data_department_have_parent(self):
        pass
