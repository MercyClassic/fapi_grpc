from typing import Literal
from uuid import UUID

from app.application.interfaces.services.main_file import MainFileServiceInterface
from httpx import AsyncClient


class MainFileService(MainFileServiceInterface):
    def __init__(self, main_file_service_addr: str) -> None:
        self._main_file_service_addr = main_file_service_addr

    async def update_file(
            self,
            file_uuid: UUID,
            status: Literal['failed', 'success'],
    ) -> None:
        async with AsyncClient() as client:
            await client.patch(
                url='%s/api/v1/files/%s' % (self._main_file_service_addr, file_uuid),
                json=status,
            )
