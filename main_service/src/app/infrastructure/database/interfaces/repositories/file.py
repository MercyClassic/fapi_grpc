from typing import Literal, Protocol
from uuid import UUID

from app.domain.models.file import FileEntity
from app.infrastructure.database.models.file import StatusEnum


class FileRepositoryInterface(Protocol):
    async def get_file(self, file_uuid: UUID) -> FileEntity:
        raise NotImplementedError

    async def save_file(self, file: FileEntity) -> None:
        raise NotImplementedError

    async def update_file_status(
            self,
            file_uuid: UUID,
            status: Literal[
                StatusEnum.failed,
                StatusEnum.success,
                StatusEnum.in_process,
            ],
    ) -> FileEntity:
        raise NotImplementedError
