import random
import string

import faker.providers


fake = faker.Faker()


class UtilProvider(faker.providers.BaseProvider):
    @staticmethod
    def string(length=10, uppercase=False, digits=False):
        letters = string.ascii_uppercase if uppercase else string.ascii_lowercase
        letters += string.digits if digits else ''
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

    @staticmethod
    def phone_number():
        """
        Random a phone number with format "84xxx"
        :return:
        """
        return '849' + ''.join([random.choice('0123456789') for _ in range(8)])


from tests.faker.company_provider import CompanyProvider
from tests.faker.department_provider import DepartmentProvider
from tests.faker.staff_provider import StaffProvider
from tests.faker.role_title_provider import RoleTitleProvider
from tests.faker.team_provider import TeamProvider
from tests.faker.location_staff_provider import LocationStaffProvider

fake.add_provider(UtilProvider)
fake.add_provider(CompanyProvider)
fake.add_provider(DepartmentProvider)
fake.add_provider(StaffProvider)
fake.add_provider(RoleTitleProvider)
fake.add_provider(TeamProvider)
fake.add_provider(LocationStaffProvider)
