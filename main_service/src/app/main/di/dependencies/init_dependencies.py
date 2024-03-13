import os
from functools import partial

from fastapi import FastAPI

from app.application.interfaces.services.file import FileServiceInterface
from app.infrastructure.database.database import (
    create_async_session_maker,
    get_async_session,
)
from app.infrastructure.database.interfaces.uow.uow import UoWInterface
from app.main.di.dependencies.file import get_file_service
from app.main.di.dependencies.stub import get_session_stub
from app.main.di.dependencies.uow import get_uow


def init_dependencies(app: FastAPI):
    async_session_maker = create_async_session_maker(os.environ['db_uri'])

    app.dependency_overrides[get_session_stub] = partial(
        get_async_session,
        async_session_maker,
    )
    app.dependency_overrides[UoWInterface] = get_uow
    app.dependency_overrides[FileServiceInterface] = get_file_service
