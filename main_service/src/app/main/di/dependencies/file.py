from typing import Annotated

from app.application.interfaces.services.log_file import LogFileServiceInterface
from app.application.services.file import FileService
from app.infrastructure.database.interfaces.uow.uow import UoWInterface
from app.infrastructure.database.repositories.file import FileRepository
from fastapi import Depends


def get_file_service(
        uow: Annotated[UoWInterface, Depends()],
        log_file_service: Annotated[LogFileServiceInterface, Depends()],
) -> FileService:
    file_repo = FileRepository(uow.session)
    return FileService(uow, file_repo, log_file_service)
