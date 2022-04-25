from typing import List

from fastapi import Request, HTTPException
from requests.models import Response

from app.core.config import settings
from app.core.security import list_email_trust
from app.helpers import generate
from app.helpers.api_handler import call_api
from app.helpers.exception_handler import CustomException
from app.schemas.sche_staff import StaffIam


class IamService(object):

    def __init__(self):
        self._api_endpoint = settings.IAM_SERVICE_URL + '/api/v1.0'
        self.all_role_sale_portal = [settings.SALE_ADMIN_ID, settings.SALE_ID,
                                     settings.SALE_LEADER_ID, settings.SALE_MANAGER_ID, settings.ADMINISTRATOR_ID]

    def get_user_by_email(self, request: Request, email: str) -> Response:
        url = self._api_endpoint + '/users'
        params = {
            'email': email
        }
        user_response = call_api(url=url,
                                 params=params, token_iam=request.headers["Authorization"])
        return user_response

    def get_id_by_email(self, request: Request, email: str) -> str:
        user_response = self.get_user_by_email(request=request, email=email)
        items = user_response.json().get("items")
        for item in items:
            if not item.get("revoked"):
                return item.get("id")

    def check_user_exist(self, request: Request, email: str):
        user_response = self.get_user_by_email(request, email)
        if user_response.status_code != 200:
            return False
        if len(user_response.json().get('items')) == 1:
            return True
        return False

    def create_user_iam(self, request: Request, user_create_request: StaffIam) -> str:
        url = self._api_endpoint + '/users'
        data = {
            "name": user_create_request.full_name,
            "password": "12345678",
            "email": user_create_request.email,
            "phone_number": user_create_request.phone_number,
            "tenant_id": "1"
        }
        reps = call_api(
            url=url, method='post', token_iam=request.headers["Authorization"], data=data)
        while reps.status_code // 100 > 2 and reps.json().get("error").get("code") == 1019:
            data["phone_number"] = generate.generate_phone_number()
            reps = call_api(url=url, method='post', token_iam=request.headers["Authorization"], data=data)
        if reps.status_code // 100 > 2:
            return None
        return reps.json().get("item").get("id")

    def crud_roles(self, request: Request, role_ids: List[int], user_id: str, method: str):
        url = self._api_endpoint + f'/users/{user_id}/roles'
        data = {
            "user_id": user_id,
            "role_ids": role_ids
        }
        call_api(
            url=url, method=method, token_iam=request.headers["Authorization"], data=data)

    def get_role_user(self, request: Request, user_id: str):
        url = self._api_endpoint + f'/users/{user_id}/roles'
        params = {
            "user_id": user_id,
        }
        reps = call_api(url=url, token_iam=request.headers["Authorization"], params=params)
        return reps.json()

    def del_all_role(self, request: Request, user_id: str):
        self.crud_roles(request, role_ids=self.all_role_sale_portal,
                        user_id=user_id, method='delete')

    def update_role(self, request: Request, role_ids: List[int], user_id: str):
        self.del_all_role(request=request, user_id=user_id)

        self.crud_roles(request=request, role_ids=role_ids,
                        user_id=user_id, method='post')

    def validate_user_can_create_user(self, request: Request):
        if not request.headers.get("Authorization"):
            raise HTTPException(status_code=403, detail="Not Authorization")
        resp = call_api(url=settings.AUTHENTICATION_SERVICE + "/userinfo",
                        token_iam=request.headers["Authorization"])
        resp = resp.json()
        # if 'email' not in resp or not resp['email'] or resp['email'] == '':
        # raise CustomException(
        # code=, detail="Không Lấy được thông tin nhân viên trên IAM")

        if resp.get("email") not in list_email_trust:
            raise CustomException(code='999', message="Không có quyền tạo mới user")
        return resp['email']
