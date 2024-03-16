from typing import Literal
from uuid import UUID

from app.application.interfaces.services.main_file import MainFileServiceInterface


class MainFileService(MainFileServiceInterface):
    async def update_file(
            self,
            file_uuid: UUID,
            status: Literal['failed', 'success'],
    ) -> None:
        pass
