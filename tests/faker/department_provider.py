import random
import logging

import faker.providers

from app.models import Department, Company
from fastapi_sqlalchemy import db

logger = logging.getLogger()
from tests.faker import fake


class DepartmentProvider(faker.providers.BaseProvider):
    @staticmethod
    def departments(company: Company, total: int = 1000):
        """
        Fake a list department in db for testing
        :return: count objects
        """
        if not company:
            company = fake.company_provider()

        departments = [Department(
            department_name=fake.job(),
            description=fake.paragraph(nb_sentences=5),
            company_id=company.id,
            is_active=bool(random.getrandbits(1))
        ) for _ in range(total)]

        with db():
            db.session.add_all(departments)
            db.session.commit()
        return len(departments)

    @staticmethod
    def department(data: dict = {}):
        """
        Fake a department in db for testing
        :return: department objects
        """
        if not data.get('company_id'):
            company = fake.company_provider()

        department = Department(
            department_name=data.get('department_name') or fake.job(),
            description=data.get('description') or fake.paragraph(nb_sentences=5),
            company_id=data.get('company_id') if data.get('company_id') else company.id,
            parent_id=data.get('parent_id') if data.get('parent_id') else None,
            is_active=data.get('is_active') if data.get('is_active') is not None else bool(random.getrandbits(1))
        )

        with db():
            db.session.add(department)
            db.session.commit()
            db.session.refresh(department)
        return department
