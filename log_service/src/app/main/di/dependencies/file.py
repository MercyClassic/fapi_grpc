from typing import Annotated

from fastapi import Depends
from odmantic.session import AIOSession

from app.application.services.file import FileService
from app.infrastructure.database.interfaces.repositories.file import (
    FileRepositoryInterface,
)
from app.infrastructure.database.repositories.file import FileRepository
from app.main.di.dependencies.stub import Stub


def get_file_repository(
        session: Annotated[AIOSession, Depends(Stub(AIOSession))],
) -> FileRepository:
    return FileRepository(session=session)


def get_file_service(
        file_repo: Annotated[FileRepositoryInterface, Depends()],
) -> FileService:
    return FileService(file_repo=file_repo)
