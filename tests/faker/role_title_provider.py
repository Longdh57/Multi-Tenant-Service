import logging
import random

import faker.providers

from app.models import RoleTitle, Company
from fastapi_sqlalchemy import db

logger = logging.getLogger()
fake = faker.Faker()


class RoleTitleProvider(faker.providers.BaseProvider):
    @staticmethod
    def role_title_provider(data={}):
        """
        Fake a role_title in db for testing
        :return: role_title model object
        """
        if not data.get('company_id'):
            company = fake.company_provider()

        role_title = RoleTitle(
            role_title_name=data.get('role_title_name') or fake.name(),
            description=data.get('description') or fake.paragraph(nb_sentences=5),
            company_id=data.get('company_id') or company.id,
            department_id=data.get('department_id') if data.get('department_id') else None,
            is_active=data.get('is_active') if data.get('is_active') is not None else bool(random.getrandbits(1))
        )
        with db():
            db.session.add(role_title)
            db.session.commit()
            db.session.refresh(role_title)
        return role_title

    @staticmethod
    def role_titles(company: Company, department_id: int = None, total: int = 50):
        """
        Fake a list role_title in db for testing
        :return: count objects
        """
        if not company:
            company = fake.company_provider()

        role_titles = [RoleTitle(
            role_title_name=fake.job(),
            description=fake.paragraph(nb_sentences=5),
            company_id=company.id,
            department_id=department_id if department_id else None,
            is_active=bool(random.getrandbits(1))
        ) for _ in range(total)]

        with db():
            db.session.add_all(role_titles)
            db.session.commit()
        return len(role_titles)
