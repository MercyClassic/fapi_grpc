from typing import Literal
from uuid import UUID, uuid4

from app.application.interfaces.services.file import FileServiceInterface
from app.application.interfaces.services.log_file import LogFileServiceInterface
from app.domain.exceptions.file import FileNotFound
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
            log_file_service: LogFileServiceInterface,
    ) -> None:
        self._uow = uow
        self._file_repo = file_repo
        self._log_file_service = log_file_service

    async def get_file(self, file_uuid: UUID) -> FileEntity:
        file = await self._file_repo.get_file(file_uuid=file_uuid)
        if not file:
            raise FileNotFound
        if file.status == 'success':
            file_data = await self._log_file_service.get_file_data(file_uuid)
            file.data = file_data
        return file

    async def create_file(self, data: dict[str, str | int]) -> FileEntity:
        file = FileEntity(uuid=uuid4(), status='in_process', data=None)
        await self._file_repo.save_file(file=file)
        await self._log_file_service.create_file(file_uuid=file.uuid, file_data=data)
        await self._uow.commit()
        return file

    async def update_file_status(
            self,
            file_uuid: UUID,
            status: Literal['failed', 'success', 'in_process'],
    ) -> FileEntity:
        file = await self._file_repo.get_file(file_uuid=file_uuid)
        if not file:
            raise FileNotFound
        file.status = status
        await self._file_repo.update_file_status(file=file)
        await self._uow.commit()
        if file.status == 'success':
            file_data = await self._log_file_service.get_file_data(file_uuid=file.uuid)
            file.data = file_data
        return file
