# import io
# import json
# import os
# import random
# from pathlib import Path
# from typing import List

# from fastapi.encoders import jsonable_encoder
# from fastapi_sqlalchemy import db
# from starlette.responses import JSONResponse
# from starlette.testclient import TestClient

# from app.core.config import settings
# from app.helpers.minio_handler import MinioHandler
# from app.models import Staff, Company, Department, RoleTitle, Team
# from app.schemas.sche_base import ResponseSchemaBase
# from tests.api import APITestCase
# from tests.faker import fake
# from app.core import message


# class TestPostStaffUploadFileAPI(APITestCase):
#     ISSUE_KEY = "O2OSTAFF-319"

#     @staticmethod
#     def create_test_data():
#         """
#         Tạo company, department, 3 role title, 3 team
#         """
#         company = fake.company_provider()
#         department = fake.department({'company_id': company.id, 'is_active': True})
#         role_titles = [
#             fake.role_title_provider({'company_id': company.id, 'department_id': department.id, 'is_active': True}) for
#             _ in range(3)]
#         teams = [fake.team({'company_id': company.id, 'is_active': True}) for _ in range(3)]
#         return company, department, role_titles, teams

#     @staticmethod
#     def upload_file(file_name: str, client: TestClient):
#         minio_client = MinioHandler().get_instance()
#         if not minio_client.check_file_name_exists(minio_client.bucket_name, file_name):
#             file = Path(os.path.join(f'tests/file_test/{file_name}'))

#             resp = client.post(f"{settings.BASE_API_PREFIX}/api/common/upload/minio", files={'file': file.open('rb')})
#             data = resp.json()
#             return data['data']['file_name']
#         else:
#             return file_name

#     def test_000_response_upload_file(self, client: TestClient):
#         """
#             Test api POST Staff Upload File response code 000
#             Step by step:
#             - Tạo company, department, role_titles, teams trong DB
#             - Call api Upload file excel danh sách nhân viên lên hệ thống
#             - Gọi API Department Add Staff với đầu vào
#             - Đầu ra mong muốn:
#                 . status code: 200
#                 . code: 000
#         """
#         file_name = 'test-danh-sach-nhan-vien.xlsx'
#         uploaded_file_path = self.upload_file(file_name=file_name, client=client)
#         company, department, role_titles, teams = self.create_test_data()

#         data_body = {
#             'company_id': company.id,
#             'file_path': uploaded_file_path
#         }
#         resp = client.post(f"{settings.BASE_API_PREFIX}/api/staffs/upload", json=jsonable_encoder(data_body))
#         data = resp.json()

#         assert resp.status_code == 200
#         assert data.get('code') == '000'
#         assert data.get('message') == 'Thành công'

#     def test_045_response_file_not_exists(self, client: TestClient):
#         """
#             Test api POST Staff Upload File response code 045
#             Step by step:
#             - Tạo company, department, role_titles, teams trong DB
#             - Gọi API Department Add Staff với đầu vào file_path ko tồn tại
#             - Đầu ra mong muốn:
#                 . status code: 400
#                 . code: 045
#         """
#         company, department, role_titles, teams = self.create_test_data()

#         data_body = {
#             'company_id': company.id,
#             'file_path': 'xxx.xlsx'
#         }
#         resp = client.post(f"{settings.BASE_API_PREFIX}/api/staffs/upload", json=jsonable_encoder(data_body))
#         data = resp.json()

#         assert resp.status_code == 400
#         assert data.get('code') == '045'
#         assert data.get('message') == 'File không tồn tại, hoặc không đúng định dạng'

#     def test_061_response_company_id_not_exists(self, client: TestClient):
#         """
#             Test api POST Staff Upload File response code 061
#             Step by step:
#             - Tạo company, department, role_titles, teams trong DB
#             - Gọi API Department Add Staff với đầu vào company_id ko tồn tại
#             - Đầu ra mong muốn:
#                 . status code: 400
#                 . code: 061
#         """
#         company, department, role_titles, teams = self.create_test_data()

#         data_body = {
#             'company_id': company.id + 1,
#             'file_path': 'xxx.xlsx'
#         }
#         resp = client.post(f"{settings.BASE_API_PREFIX}/api/staffs/upload", json=jsonable_encoder(data_body))
#         data = resp.json()

#         assert resp.status_code == 400
#         assert data.get('code') == '061'
#         assert data.get('message') == 'ID company không tồn tại trong hệ thống'

#     def test_139_response_file_wrong_template(self, client: TestClient):
#         """
#             Test api POST Staff Upload File response code 139
#             Step by step:
#             - Tạo company, department, role_titles, teams trong DB
#             - Call api Upload file excel danh sách nhân viên lên hệ thống với file sai định dạng
#             - Gọi API Department Add Staff với đầu vào
#             - Đầu ra mong muốn:
#                 . status code: 400
#                 . code: 139
#         """
#         file_name = 'testing-danh-sach-nhan-vien-wrong-format.xlsx'
#         uploaded_file_path = self.upload_file(file_name=file_name, client=client)
#         company, department, role_titles, teams = self.create_test_data()

#         data_body = {
#             'company_id': company.id,
#             'file_path': uploaded_file_path
#         }
#         resp = client.post(f"{settings.BASE_API_PREFIX}/api/staffs/upload", json=jsonable_encoder(data_body))
#         data = resp.json()

#         assert resp.status_code == 400
#         assert data.get('code') == '139'
#         assert data.get('message') == 'File không đúng template'

#     def test_000_response_with_code_140_file_error_data(self, client: TestClient):
#         """
#             Test api POST Staff Upload File response code 140
#             Step by step:
#             - Tạo company, department, role_titles, teams trong DB
#             - Call api Upload file excel danh sách nhân viên lên hệ thống với file sai data
#             - Gọi API Department Add Staff với đầu vào
#             - Đầu ra mong muốn:
#                 . status code: 200
#                 . code: 140
#         """
#         file_name = 'test-danh-sach-nhan-vien-error-data.xlsx'
#         uploaded_file_path = self.upload_file(file_name=file_name, client=client)
#         company, department, role_titles, teams = self.create_test_data()

#         data_body = {
#             'company_id': company.id,
#             'file_path': uploaded_file_path
#         }
#         resp = client.post(f"{settings.BASE_API_PREFIX}/api/staffs/upload", json=jsonable_encoder(data_body))
#         data = resp.json()

#         assert resp.status_code == 200
#         assert data.get('code') == '140'
#         assert data.get('message') == 'Lỗi dữ liệu, vui lòng check trong file kết quả lỗi'

#     def test_999_internal_error(self, client: TestClient):
#         """
#             Test api get staff List response code 999
#             Step by step:
#             - Gọi API staff List lỗi
#             - Đầu ra mong muốn:
#                 . status code: 500
#                 . code: 999
#         """
#         res = JSONResponse(
#             status_code=500,
#             content=jsonable_encoder(
#                 ResponseSchemaBase().custom_response(
#                     '999', "Hệ thống đang bảo trì, quý khách vui lòng thử lại sau"
#                 )
#             )
#         )
#         assert res.status_code == 500 and json.loads(res.body) == {
#             "code": "999",
#             "message": "Hệ thống đang bảo trì, quý khách vui lòng thử lại sau"
#         }
