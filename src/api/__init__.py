from fastapi import APIRouter

from src.api.users import users_router as users_router
from src.api.reports import reports_router
from src.api.dev import developer_router

from src.config import settings

main_router = APIRouter()
if settings.dev_routes_enabled:
    main_router.include_router(developer_router, prefix="/dev", tags=["Developer"])

main_router.include_router(users_router, tags=["Users"])
main_router.include_router(reports_router, tags=["Reports"])