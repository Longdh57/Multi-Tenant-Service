import logging
from typing import List

from fastapi_sqlalchemy import db

from app.models import Corporation, Company
from app.schemas.sche_corporation import CorporationItemResponse
from app.services.srv_base import BaseService

logger = logging.getLogger()


class CorporationService(BaseService):

    def __init__(self):
        super().__init__(Corporation)

    def get_list_corporation(self) -> List[CorporationItemResponse]:
        corporations = db.session.query(Corporation).all()

        company_datas = db.session.query(Company).filter(
            Company.corporation_id.in_([corporation.id for corporation in corporations])).all()

        for corporation in corporations:
            companies = [company for company in company_datas if company.corporation_id == corporation.id]
            corporation = corporation.__dict__
            corporation["companies"] = companies

        return corporations

    def get_list_company(self, corporation: Corporation):
        return db.session.query(Company).filter(Company.corporation_id == corporation.id).all()


corporation_service = CorporationService()
