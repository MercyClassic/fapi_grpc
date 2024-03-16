from abc import abstractmethod
from typing import Literal, Protocol
from uuid import UUID


class MainFileServiceInterface(Protocol):
    @abstractmethod
    async def update_file(
            self,
            file_uuid: UUID,
            status: Literal['failed', 'success'],
    ) -> None:
        raise NotImplementedError
