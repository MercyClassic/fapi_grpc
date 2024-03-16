from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends

from app.application.interfaces.services.file import FileServiceInterface
from app.application.models.file import FileIn, FileOut
from app.main.di.dependencies.stub import Stub

router = APIRouter(
    responses={
        404: {
            'description': 'File not found',
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
        file_service: Annotated[FileServiceInterface, Depends(Stub(FileServiceInterface))],
) -> Any:
    file = await file_service.get_file(file_uuid)
    return file


@router.post(
    '/files',
    response_model=FileOut,
    status_code=201,
)
async def save_file(
        file_in: FileIn,
        file_service: Annotated[FileServiceInterface, Depends(Stub(FileServiceInterface))],
) -> Any:
    file = await file_service.create_file(
        file_uuid=file_in.uuid,
        data=file_in.data,
    )
    return file
