from tests.faker import fake
import random
import logging

import faker.providers

from app.models import Team, Staff, Company
from fastapi_sqlalchemy import db

logger = logging.getLogger()


class TeamProvider(faker.providers.BaseProvider):

    @staticmethod
    def teams(company: Company, total: int = 40):
        if not company:
            company = fake.company_provider()
        teams = [Team(
            team_name=fake.job(),
            description=fake.paragraph(nb_sentences=5),
            company_id=company.id,
            is_active=True
        ) for _ in range(total)]

        with db():
            db.session.add_all(teams)
            db.session.commit()
        return len(teams)

    @staticmethod
    def team(data: dict = {}):
        if not data.get('company_id'):
            company = fake.company_provider()

        team = Team(
            team_name=data.get('team_name') or fake.unique.job(),
            description=data.get(
                'description') or fake.paragraph(nb_sentences=5),
            company_id=data.get('company_id') or company.id,
            is_active=data.get('is_active') if data.get(
                'is_active') is not None else True
        )
        with db():
            db.session.add(team)
            db.session.commit()
            db.session.refresh(team)
        return team
