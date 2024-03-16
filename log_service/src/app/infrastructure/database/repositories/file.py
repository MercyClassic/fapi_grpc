from uuid import UUID

from odmantic.session import AIOSession

from app.domain.models.file import FileEntity
from app.infrastructure.database.interfaces.repositories.file import (
    FileRepositoryInterface,
)
from app.infrastructure.database.models.file import File


class FileRepository(FileRepositoryInterface):
    def __init__(self, session: AIOSession):
        self._session = session

    async def get_file(self, file_uuid: UUID) -> FileEntity | None:
        file = await self._session.find_one(File, File.uuid == str(file_uuid))
        if file:
            return self._serialize_file(file)

    async def save_file(self, file: FileEntity) -> None:
        db_file = File(uuid=file.uuid, data=file.data)
        await self._session.save(db_file)

    def _serialize_file(self, file: File) -> FileEntity:
        return FileEntity(
            uuid=file.uuid,
            data=file.data,
        )
