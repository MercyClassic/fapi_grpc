from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from app.domain.models.file import FileEntity


class FileServiceInterface(Protocol):
    @abstractmethod
    async def get_file(self, file_uuid: UUID) -> FileEntity:
        raise NotImplementedError

    @abstractmethod
    async def create_file(
            self,
            file_uuid: UUID,
            data: dict[str, str | int],
    ) -> FileEntity:
        raise NotImplementedError
