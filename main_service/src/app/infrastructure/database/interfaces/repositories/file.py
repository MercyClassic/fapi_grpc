from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from app.domain.models.file import FileEntity


class FileRepositoryInterface(Protocol):
    @abstractmethod
    async def get_all_files(self) -> list[FileEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_file(self, file_uuid: UUID) -> FileEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def save_file(self, file: FileEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_file_status(
            self,
            file: FileEntity,
    ) -> None:
        raise NotImplementedError
