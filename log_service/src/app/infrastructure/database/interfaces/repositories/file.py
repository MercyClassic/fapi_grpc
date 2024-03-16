from typing import Protocol
from uuid import UUID

from app.domain.models.file import FileEntity


class FileRepositoryInterface(Protocol):
    async def get_file(self, file_uuid: UUID) -> FileEntity | None:
        raise NotImplementedError

    async def save_file(self, file: FileEntity) -> None:
        raise NotImplementedError
