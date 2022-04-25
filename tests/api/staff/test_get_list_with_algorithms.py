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
    ISSUE_KEY = "O2OSTAFF-634"

    def test_get_with_algorithms_HR(self, client: TestClient):
        pass

    def test_get_with_algorithms_SP(self, client: TestClient):
        pass
