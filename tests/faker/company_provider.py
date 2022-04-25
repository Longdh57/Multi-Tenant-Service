import logging
import faker.providers

from app.models import Company
from fastapi_sqlalchemy import db

logger = logging.getLogger()
fake = faker.Faker()


class CompanyProvider(faker.providers.BaseProvider):
    @staticmethod
    def company_provider(data={}):
        """
        Fake a company in db for testing
        :return: company model object
        """
        company = Company(
            company_code=data.get('company_code') or fake.name(),
            company_name=data.get('company_name') or fake.company(),
            description=data.get('description') or fake.paragraph(nb_sentences=5)
        )
        with db():
            db.session.add(company)
            db.session.commit()
            db.session.refresh(company)
        return company
