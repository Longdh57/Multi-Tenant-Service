from typing import List

from fastapi import Request
from fastapi_sqlalchemy import db

from app.core.config import settings
from app.helpers.enums import SalesRoleName
from app.models import Staff, RoleTitle, DepartmentStaff
from app.schemas.sche_staff import StaffIam, StaffIamUploadFile
from app.services.srv_iam import IamService

STAFF = 0
DEPARMENT_STAFF = 2
ROLE_TITLE = 2


def synchronized_srv(request: Request):
    print("Start")
    create_user, update_user = set(), []
    iam_srv = IamService()
    # iam_srv.validate_user_can_create_user(request)
    tables = db.session.query(Staff, DepartmentStaff, RoleTitle) \
        .filter(Staff.id == DepartmentStaff.staff_id) \
        .filter(DepartmentStaff.role_title_id == RoleTitle.id) \
        .filter(Staff.is_active) \
        .filter(DepartmentStaff.is_active) \
        .filter(RoleTitle.role_title_name.in_(SalesRoleName.get_list_value())).all()

    for table in tables:
        staff = table[STAFF]
        exist_user = iam_srv.get_id_by_email(request, staff.email)
        if exist_user is None:
            create_user.add(table)
        else:
            roles = iam_srv.get_role_user(request, exist_user).get("items")
            role_name = table[ROLE_TITLE].role_title_name
            if not check_role_update(roles, role_name, iam_srv):
                update_user.append({"user_id": exist_user, "roles": get_role_id_iam(role_name)})

    for user in create_user:
        staff_iam_create = StaffIam(
            email=user[STAFF].email,
            full_name=user[STAFF].full_name,
            phone_number=user[STAFF].phone_number
        )
        user_id = iam_srv.create_user_iam(request=request, user_create_request=staff_iam_create)
        # print(type(user_create))
        update_user.append({"user_id": user_id, "roles": get_role_id_iam(user[ROLE_TITLE].role_title_name)})
    for user in update_user:
        iam_srv.update_role(request=request, role_ids=[user.get("roles")], user_id=user.get("user_id"))
    print("Finished")


def synchronized_upload_excel(request, staffs: List[StaffIamUploadFile]):
    iam_srv = IamService()
    for staff in staffs:
        user_id = iam_srv.create_user_iam(request=request, user_create_request=staff)
        if user_id is None:
            user_id = iam_srv.get_id_by_email(request=request, email=staff.email)
        role_ids = [get_role_id_iam(staff.role)]
        iam_srv.update_role(request, role_ids=role_ids, user_id=user_id)


def check_role_update(roles: list, user_role: str, iam_srv: IamService):
    for role in roles:
        id_role = role.get("id")
        if id_role in iam_srv.all_role_sale_portal:
            if (user_role == SalesRoleName.SALE.value and id_role == settings.SALE_ID) \
                    or (user_role == SalesRoleName.SALE_ADMIN.value and id_role == settings.SALE_ADMIN_ID) \
                    or (user_role == SalesRoleName.SALE_LEADER.value and id_role == settings.SALE_LEADER_ID) \
                    or (user_role == SalesRoleName.SALE_MANAGER.value and id_role == settings.SALE_MANAGER_ID):
                return True
    return False


def get_role_id_iam(role_name):
    if role_name == SalesRoleName.SALE.value:
        return settings.SALE_ID
    if role_name == SalesRoleName.SALE_ADMIN.value:
        return settings.SALE_ADMIN_ID
    if role_name == SalesRoleName.SALE_LEADER.value:
        return settings.SALE_LEADER_ID
    if role_name == SalesRoleName.SALE_MANAGER.value:
        return settings.SALE_MANAGER_ID
    if role_name == SalesRoleName.ADMINISTRATOR.value:
        return settings.ADMINISTRATOR_ID
