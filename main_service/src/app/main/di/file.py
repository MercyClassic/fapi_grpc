from typing import Annotated

from fastapi import Depends

from app.application.services.file import FileService
from app.application.services.log_file import LogFileServiceInterface
from app.infrastructure.database.repositories.file import FileRepository
from app.infrastructure.database.uow import UoWInterface


def get_file_service(
        uow: Annotated[UoWInterface, Depends()],
        log_file_service: Annotated[LogFileServiceInterface, Depends()],
) -> FileService:
    file_repo = FileRepository(uow.session)
    return FileService(uow, file_repo, log_file_service)
