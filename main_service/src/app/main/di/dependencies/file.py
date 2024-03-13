from typing import Annotated

from fastapi import Depends

from app.application.services.file import FileService
from app.infrastructure.database.interfaces.uow.uow import UoWInterface
from app.infrastructure.database.repositories.file import FileRepository


def get_file_service(
        uow: Annotated[UoWInterface, Depends()],
) -> FileService:
    file_repo = FileRepository(uow.session)
    return FileService(uow, file_repo)
