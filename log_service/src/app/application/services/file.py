import json
from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from aiokafka import AIOKafkaProducer

from app.domain.exceptions.file import FileNotFound
from app.domain.models.file import FileEntity
from app.infrastructure.database.repositories.file import FileRepositoryInterface


class FileServiceInterface(Protocol):
    @abstractmethod
    async def get_file(self, file_uuid: UUID) -> FileEntity:
        raise NotImplementedError

    @abstractmethod
    async def create_file(
        self,
        file_uuid: UUID,
        data: dict[str, str | int | dict],
    ) -> FileEntity:
        raise NotImplementedError


class FileService(FileServiceInterface):
    def __init__(
        self,
        file_repo: FileRepositoryInterface,
        bus_producer: AIOKafkaProducer,
    ) -> None:
        self._file_repo = file_repo
        self._bus_producer = bus_producer

    async def get_file(self, file_uuid: UUID) -> FileEntity:
        file = await self._file_repo.get_file(file_uuid=file_uuid)
        if not file:
            raise FileNotFound
        return file

    async def create_file(
        self,
        file_uuid: UUID,
        data: dict[str, str | int],
    ) -> FileEntity:
        file = FileEntity(uuid=file_uuid, data=data)
        await self._file_repo.save_file(file=file)
        value = json.dumps({'uuid': str(file.uuid), 'data': file.data}).encode()
        await self._bus_producer.send_and_wait(
            topic='logger_topic',
            value=value,
        )
        return file
