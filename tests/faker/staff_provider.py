import logging
import random
from datetime import datetime, timedelta

import faker.providers

from app.helpers.enums import StaffContractType
from app.models import Staff, CompanyStaff
from app.models import Team, Company, CompanyStaff, StaffTeam, Department, DepartmentStaff, RoleTitle

from fastapi_sqlalchemy import db

logger = logging.getLogger()
fake = faker.Faker()


class StaffProvider(faker.providers.BaseProvider):

    @staticmethod
    def add_staff_to_team(company: Company, team: Team):
        if not company:
            company = fake.company_provider()
        if not team:
            team = fake.team({'company_id': company.id})
        staff = StaffProvider.staff_provider({'company_id': company.id})
        staff_team = StaffTeam(
            staff_id=staff.id,
            team_id=team.id
        )
        with db():
            db.session.add(staff_team)
            db.session.commit()
            db.session.refresh(staff_team)

    @staticmethod
    def add_staff_to_teams(company: Company, staff: Staff, total_team: int = 10):
        if not company:
            company = fake.company_provider()
        if not staff:
            staff = StaffProvider.staff_provider({'company_id': company.id})
        for i in range(total_team):
            staff = StaffProvider.staff_provider({'company_id': company.id})
            team = fake.team({'company_id': company.id})
            staff_team = StaffTeam(
                staff_id=staff.id,
                team_id=team.id
            )
            db.session.add(staff_team)
        with db():
            db.session.commit()
            db.session.refresh(staff_team)

    @staticmethod
    def add_staff_to_department(company: Company, staff: Staff, department: Department = None, role_title: RoleTitle = None):
        if not company:
            company = fake.company_provider()
        if not staff:
            staff = StaffProvider.staff_provider({'company_id': company.id})
        if not department:
            department = fake.department({'company_id': company.id})
        if not role_title:
            role_title = fake.role_title_provider(
                {'company_id': company.id, 'department_id': department.id})
        department_staff = DepartmentStaff(
            department_id=department.id,
            staff_id=staff.id,
            role_title_id=role_title.id,
            is_active=True,
        )
        with db():
            db.session.add(department_staff)
            db.session.commit()
            db.session.refresh(department_staff)
        return staff

    @staticmethod
    def staff_provider(data={}):
        """
        Fake a staff in db for testing
        :return: staff model object
        """
        company = None
        if not data.get('company_id'):
            company = fake.company_provider()

        staff = Staff(
            id=data.get('id') if data.get('id') else None,
            full_name=data.get('full_name') or fake.name(),
            staff_code=data.get('staff_code') or fake.ean8(),
            date_of_birth=data.get('date_of_birth') or fake.date(),
            email_personal=data.get('email_personal') or fake.email(),
            email=data.get('email') or fake.email(),
            phone_number=data.get('phone_number') or fake.phone_number(),
            manager_id=data.get('manager_id') if data.get(
                'manager_id') else None,
            company_id=data.get('company_id') or company.id,
            date_onboard=data.get('date_onboard') or (
                datetime.now() - timedelta(days=random.randint(99, 2000))).date(),
            bank_name=data.get('bank_name') or random.choice(
                ['Vietcombank', 'MB Bank', 'Vietinbank', 'Bidv']),
            branch_bank_name=data.get('branch_bank_name') or fake.city(),
            account_number=data.get('account_number') or fake.bban(),
            address_detail=data.get('address_detail') or fake.address(),
            identity_card=data.get('identity_card') or random.randint(
                999999999, 999999999999),
            contract_type=data.get(
                'contract_type') or StaffContractType.OFFICIAL.value,
            is_active=data.get('is_active') if data.get(
                'is_active') is not None else True
        )
        with db():
            db.session.add(staff)
            db.session.commit()
            db.session.refresh(staff)

        company_staff = CompanyStaff(
            company_id=data.get('company_id') or company.id,
            staff_id=staff.id,
            email=staff.email,
            is_active=staff.is_active
        )
        with db():
            db.session.add(company_staff)
            db.session.commit()
        
        return staff

    @staticmethod
    def create_staff_request(data={}):
        if not data.get('company_id'):
            company = fake.company_provider()
        company_id = data.get('company_id') or company.id
        if not data.get('deparment_id'):
            deparment = fake.deparment({'company_id': company_id})
        deparment_id = data.get('deparment_id') or deparment.id
        if not data.get('role_title_id'):
            role_title = fake.role_title_provider(
                {'company_id': company_id, 'deparment_id': deparment_id})
        role_title_id = data.get('role_title_id') or role_title.id

        if not data.get('team'):
            pass
        staff = {
            'full_name': data.get('full_name') or fake.name(),
            'staff_code': data.get('staff_code') or fake.ean8(),
            'date_of_birth': data.get('date_of_birth') or fake.date(),
            'email_personal': data.get('email_personal') or fake.email(),
            'email': data.get('email') or fake.email(),
            'phone_number': data.get('phone_number') or fake.phone_number(),
            'manager_id': data.get('manager_id') if data.get(
                'manager_id') else None,
            'company_id': data.get('company_id') or company.id,
            'date_onboard': data.get('date_onboard') or (
                datetime.now() - timedelta(days=random.randint(99, 2000))).date(),
            'bank_name': data.get('bank_name') or random.choice(
                ['Vietcombank', 'MB Bank', 'Vietinbank', 'Bidv']),
            'branch_bank_name': data.get('branch_bank_name') or fake.city(),
            'account_number': data.get('account_number') or fake.bban(),
            'address_detail': data.get('address_detail') or fake.address(),
            'identity_card': data.get('identity_card') or random.randint(
                999999999, 999999999999),
            'contract_type': data.get(
                'contract_type') or StaffContractType.OFFICIAL.value,
            'is_active': data.get('is_active') if data.get(
                'is_active') is not None else bool(random.getrandbits(1)),
            'department': {
                'department_id': deparment_id,
                'role_title_id': role_title_id,
                'is_active': True
            },
        }
        return staff
