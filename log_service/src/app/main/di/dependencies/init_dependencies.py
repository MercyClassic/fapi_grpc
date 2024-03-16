import os
from functools import partial

from fastapi import FastAPI
from odmantic.session import AIOSession

from app.application.interfaces.services.file import FileServiceInterface
from app.infrastructure.database.database import create_engine, get_session
from app.infrastructure.database.interfaces.repositories.file import (
    FileRepositoryInterface,
)
from app.main.di.dependencies.file import get_file_repository, get_file_service


def init_dependencies(app: FastAPI) -> None:
    engine = create_engine(
        db_uri=os.environ['mongo_db_uri'],
        db_name=os.environ['mongo_db_name'],
    )
    app.dependency_overrides[AIOSession] = partial(get_session, engine)
    app.dependency_overrides[FileRepositoryInterface] = get_file_repository
    app.dependency_overrides[FileServiceInterface] = get_file_service
