from fastapi import APIRouter

from app.api.base import api_healthcheck, api_company

router = APIRouter()

router.include_router(api_healthcheck.router, tags=["healthcheck"], prefix="/healthcheck")
# router.include_router(api_common.router, tags=["common"], prefix="/common")
router.include_router(api_company.router, tags=["company"], prefix="/companies")
