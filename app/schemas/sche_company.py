from datetime import datetime
from typing import Optional

from pydantic import BaseModel, root_validator

from app.core import error_code, message
from app.helpers.exception_handler import ValidateException
from app.helpers.paging import PaginationParams


class CompanyListRequest(PaginationParams):
    pass


class CompanyBase(BaseModel):
    company_name: Optional[str] = None

    class Config:
        orm_mode = True


class CompanyIdNotRequest(BaseModel):
    company_id: Optional[int]


class CompanyIdRequest(BaseModel):
    company_id: Optional[int]

    @root_validator()
    def params_valid(cls, params):
        company_id = params.get('company_id')
        if not company_id:
            raise ValidateException(error_code.ERROR_092_COMPANY_ID_IS_REQUIRED,
                                    message.MESSAGE_092_COMPANY_ID_IS_REQUIRED)
        return params


class CompanyId(BaseModel):
    company_id: Optional[int]


class CompanyItemResponse(CompanyBase):
    class Corporation(BaseModel):
        id: int
        corporation_name: str

        class Config:
            orm_mode = True

    id: int
    company_name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    corporation: Optional[Corporation]
