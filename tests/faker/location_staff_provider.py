from typing import List, Optional

from tests.faker import fake
import random
import logging

import faker.providers

from app.models import Team, Staff, Company, LocationStaff
from fastapi_sqlalchemy import db

logger = logging.getLogger()


class LocationStaffProvider(faker.providers.BaseProvider):

    @staticmethod
    def location_staffs(staff: Staff = None):
        if staff is None:
            company = fake.company_provider()
            staff = fake.staff_provider(data={'company_id': company.id})
        location_staffs = [
            LocationStaff(
                location_code='01',
                location_name='Thành phố Hà Nội',
                staff_id=staff.id
            ),
            LocationStaff(
                location_code='79',
                location_name='Thành phố Hồ Chí Minh',
                staff_id=staff.id
            ),
            LocationStaff(
                location_code='48',
                location_name='Thành phố Đà Nẵng'
            )
        ]

        with db():
            db.session.add_all(location_staffs)
            db.session.commit()
        return location_staffs
