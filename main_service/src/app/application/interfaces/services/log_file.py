from abc import abstractmethod
from typing import Protocol
from uuid import UUID


class LogFileServiceInterface(Protocol):
    @abstractmethod
    async def get_file_data(self, file_uuid: UUID) -> dict[str, str | int | dict]:
        raise NotImplementedError

    @abstractmethod
    async def create_file(
            self,
            file_uuid: UUID,
            file_data: dict[str, str | int | dict],
    ) -> dict[str, str | int | dict]:
        raise NotImplementedError
