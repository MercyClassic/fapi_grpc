from typing import Literal
from uuid import UUID

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.file import FileEntity
from app.infrastructure.database.interfaces.repositories.file import (
    FileRepositoryInterface,
)
from app.infrastructure.database.models.file import File, StatusEnum


class FileRepository(FileRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_file(self, file_uuid: UUID) -> FileEntity:
        query = select(File).where(File.uuid == file_uuid)
        result = await self._session.execute(query)
        return result.scalar()

    async def save_file(self, file: FileEntity) -> None:
        stmt = insert(File).values(status='in_process').returning(File)
        result = await self._session.execute(stmt)
        file.uuid = result.scalar().uuid

    async def update_file_status(
            self,
            file_uuid: UUID,
            status: Literal[
                StatusEnum.failed,
                StatusEnum.success,
                StatusEnum.in_process,
            ],
    ) -> FileEntity:
        stmt = update(File).values(status=status).where(file_uuid=file_uuid).returning(File)
        file = await self._session.execute(stmt)
        return self._serialize_file(file)

    def _serialize_file(self, file: File) -> FileEntity:
        return FileEntity(
            uuid=file.uuid,
            status=file.status,
        )
