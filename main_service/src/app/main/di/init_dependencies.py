import os
from functools import partial

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.services.file import FileServiceInterface
from app.application.services.log_file import LogFileServiceInterface
from app.infrastructure.database.database import (
    create_async_session_maker,
    get_async_session,
)
from app.infrastructure.database.uow import UoWInterface
from app.main.di.file import get_file_service
from app.main.di.log_file import get_log_file_service
from app.main.di.uow import get_uow


def init_dependencies(app: FastAPI):
    async_session_maker = create_async_session_maker(os.environ['db_uri'])

    app.dependency_overrides[AsyncSession] = partial(
        get_async_session,
        async_session_maker,
    )
    app.dependency_overrides[UoWInterface] = get_uow
    app.dependency_overrides[FileServiceInterface] = get_file_service
    app.dependency_overrides[LogFileServiceInterface] = partial(
        get_log_file_service,
        os.environ['LOG_FILE_SERVICE_ADDR'],
    )
