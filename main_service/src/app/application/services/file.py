from typing import Literal
from uuid import UUID

from app.application.interfaces.services.file import FileServiceInterface
from app.domain.models.file import FileEntity
from app.infrastructure.database.interfaces.repositories.file import (
    FileRepositoryInterface,
)
from app.infrastructure.database.interfaces.uow.uow import UoWInterface


class FileService(FileServiceInterface):
    def __init__(
            self,
            uow: UoWInterface,
            file_repo: FileRepositoryInterface,
    ) -> None:
        self._uow = uow
        self._file_repo = file_repo

    async def get_file(self, file_uuid: UUID) -> FileEntity:
        file = self._file_repo.get_file(file_uuid=file_uuid)
        ...  # todo: join data from another service
        return file

    async def create_file(self, data: dict[str, str | int]) -> FileEntity:
        file = FileEntity(uuid=None, data=data)
        await self._file_repo.save_file(file=file)
        ...  # todo: send save file request to another log-service

    async def update_file_status(
            self,
            file_uuid: UUID,
            status: Literal['failed', 'success', 'in_process'],
    ) -> FileEntity:
        file = await self._file_repo.update_file_status(file_uuid=file_uuid, status=status)
        ...  # todo: join data from another service
        return file
