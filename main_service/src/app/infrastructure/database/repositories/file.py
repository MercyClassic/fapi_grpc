from uuid import UUID

from app.domain.models.file import FileEntity
from app.infrastructure.database.interfaces.repositories.file import (
    FileRepositoryInterface,
)
from app.infrastructure.database.models.file import File
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class FileRepository(FileRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_file(self, file_uuid: UUID) -> FileEntity | None:
        query = select(File).where(File.uuid == file_uuid)
        result = await self._session.execute(query)
        result = result.scalar()
        if result:
            return self._serialize_file(result)

    async def save_file(self, file: FileEntity) -> None:
        stmt = insert(File).values(uuid=file.uuid, status='in_process').returning(File)
        result = await self._session.execute(stmt)
        file.uuid = result.scalar().uuid

    async def update_file_status(
            self,
            file: FileEntity,
    ) -> None:
        stmt = update(File).values(status=file.status).where(File.uuid == file.uuid)
        await self._session.execute(stmt)

    def _serialize_file(self, file: File) -> FileEntity:
        return FileEntity(
            uuid=file.uuid,
            status=file.status.value,
            data=None,
        )
