import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.helpers.paging import PaginationParams, paginate, Page
from app.models import Company
from app.schemas.sche_company import CompanyItemResponse

logger = logging.getLogger()
router = APIRouter()


@router.get("", response_model=Page[CompanyItemResponse])
def get(company_list_req: PaginationParams = Depends(), db: Session = Depends(get_db)) -> Any:
    """
    API Get list Company by Tenant
    """
    try:
        _query = db.query(Company)
        companies = paginate(model=Company, query=_query, params=company_list_req)
        return companies
    except Exception as e:
        return HTTPException(status_code=400, detail=logger.error(e))
