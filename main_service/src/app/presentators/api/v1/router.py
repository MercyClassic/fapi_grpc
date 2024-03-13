from fastapi import APIRouter

from app.presentators.api.v1.file import router as core_router

v1_router = APIRouter(prefix='/api/v1')
v1_router.include_router(core_router)
