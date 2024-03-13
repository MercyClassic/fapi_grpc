from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Body, Depends

from app.application.interfaces.services.file import FileServiceInterface
from app.application.models.core import FileIn, FileOut

router = APIRouter(
    tags=['core'],
    responses={
        404: {
            'description': 'File Not Found',
            'content': {
                'application/json': {
                    'example': {'detail': 'File not found'},
                },
            },
        },
    },
)


@router.get(
    '/files/{file_uuid}',
    response_model=FileOut,
    status_code=200,
)
async def get_file(
        file_uuid: UUID,
        file_service: Annotated[FileServiceInterface, Depends()],
) -> Any:
    file = await file_service.get_file(file_uuid=file_uuid)
    return file


@router.patch(
    '/files/{file_uuid}',
    status_code=200,
)
async def update_file_status(
        file_uuid: UUID,
        file_service: Annotated[FileServiceInterface, Depends()],
        status: Annotated[str, Body()],
) -> Any:
    await file_service.update_file_status(file_uuid=file_uuid, status=status)


@router.post(
    '/files',
    response_model=FileOut,
    status_code=201,
)
async def create_file(
        file: FileIn,
        file_service: Annotated[FileServiceInterface, Depends()],
) -> Any:
    file = await file_service.create_file(file=file)
    return file
