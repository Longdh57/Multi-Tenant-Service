from sqlalchemy import text
from fastapi_sqlalchemy import db

from app.core import error_code, message
from app.core.config import settings
from app.helpers.api_handler import call_api
from app.helpers.exception_handler import CustomException
from app.models import Staff, LocationStaff
from app.schemas.sche_location_staff import LocationStaffListRequest, UpdateStaffLocationRequest
from app.services.srv_base import BaseService


class LocationStaffService(BaseService):
    def __init__(self):
        super().__init__(LocationStaff)
        self._api_endpoint = settings.LOCATION_SERVICE_URL

    def get_list(self, ls_list_req: LocationStaffListRequest):
        _query = db.session.query(LocationStaff)
        if ls_list_req.provinceCode is not None:
            _query = db.session.query(LocationStaff).filter(LocationStaff.location_code == ls_list_req.provinceCode)
        location_staffs = _query.order_by(LocationStaff.id.asc()).all()
        if len(location_staffs) == 0:
            if ls_list_req.provinceCode is not None:  # neu ko tim thay provinceCode, raise loi
                raise CustomException(
                    http_code=400,
                    code=error_code.ERROR_200_PROVINCE_CODE_NOT_EXITS,
                    message=message.MESSAGE_200_PROVINCE_CODE_NOT_EXITS
                )
            else:
                self.initial_data()
                location_staffs = db.session.query(LocationStaff).all()
        list_staff = [location_staff.staff_id for location_staff in location_staffs]
        staffs = db.session.query(Staff).filter(Staff.id.in_(list_staff)).all()
        location_staff_resp = []
        for location_staff in location_staffs:
            if location_staff.staff_id is None:
                if ls_list_req.provinceCode is not None:
                    # Nếu location chưa có sale-admin thì return mặc định env.LOCATION_ADMINISTRATOR
                    staff_admin = db.session.query(Staff).get(settings.LOCATION_ADMINISTRATOR)
                    location_staff_resp.append(dict(
                        province_code=location_staff.location_code,
                        province_name=location_staff.location_name,
                        staff_id=staff_admin.id,
                        staff_email=staff_admin.email,
                        staff_full_name=staff_admin.full_name
                    ))
                    break
                else:
                    location_staff_resp.append(dict(
                        province_code=location_staff.location_code,
                        province_name=location_staff.location_name
                    ))
            else:
                for staff in staffs:
                    if staff.id == location_staff.staff_id:
                        location_staff_resp.append(dict(
                            province_code=location_staff.location_code,
                            province_name=location_staff.location_name,
                            staff_id=staff.id,
                            staff_email=staff.email,
                            staff_full_name=staff.full_name
                        ))

        return location_staff_resp

    def initial_data(self):
        sql = text(f'Truncate table {LocationStaff.__tablename__}')
        db.session.execute(sql)
        provinces = self.get_list_province()
        location_staffs = []
        for province in provinces:
            location_staffs.append(
                LocationStaff(
                    location_code=province.get('code'),
                    location_name=province.get('name'),
                )
            )
        db.session.add_all(location_staffs)
        db.session.commit()

    def get_list_province(self):
        url = self._api_endpoint + '/v1/location/provinces'

        resp = call_api(method='get', url=url)
        if resp.status_code != 200:
            raise CustomException(code='500', message=f"Lỗi kết nối đến {self._api_endpoint}")

        provinces = []
        for data in resp.json()['result']['provinces']:
            provinces.append({
                'code': data['code'],
                'name': data['name'],
                'region': data['region'],
            })
        return provinces

    def update_mapping_staff_location(self, request_data: UpdateStaffLocationRequest):
        location = db.session.query(LocationStaff).filter(LocationStaff.location_code == request_data.provinceCode).first()
        
        if location is not None:
            try:
                location.staff_id = request_data.staffId
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise CustomException(
                    http_code=400, code=error_code.ERROR_999_SERVER, message=message.MESSAGE_999_SERVER)
        else:
            raise CustomException(
                http_code=400,
                code=error_code.ERROR_200_PROVINCE_CODE_NOT_EXITS,
                message=message.MESSAGE_200_PROVINCE_CODE_NOT_EXITS
            )
