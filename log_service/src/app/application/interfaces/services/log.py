from abc import abstractmethod
from datetime import datetime
from typing import Protocol

from app.domain.models.file import FileEntity


class LogFileServiceInterface(Protocol):
    @abstractmethod
    async def process_logging(self, file: FileEntity, dt: datetime) -> None:
        raise NotImplementedError
