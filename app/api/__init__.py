from fastapi import APIRouter

from .base.router import router as base_router

router = APIRouter()

router.include_router(base_router, prefix='/api')
