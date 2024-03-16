from fastapi import APIRouter

from app.presentators.api.v1.file import router as file_router

v1_router = APIRouter(prefix='/api/v1')
v1_router.include_router(file_router)
