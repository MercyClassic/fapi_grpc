from typing import Annotated, Any, Literal
from uuid import UUID

from app.application.interfaces.services.file import FileServiceInterface
from app.application.models.file import FileIn, FileOut
from app.main.di.dependencies.stub import Stub
from fastapi import APIRouter, Body, Depends

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
    '/files',
    response_model=list[FileOut],
    status_code=200,
)
async def get_all_files(
        file_service: Annotated[FileServiceInterface, Depends(Stub(FileServiceInterface))],
) -> Any:
    file = await file_service.get_all_files()
    return file


@router.get(
    '/files/{file_uuid}',
    response_model=FileOut,
    status_code=200,
)
async def get_file(
        file_uuid: UUID,
        file_service: Annotated[FileServiceInterface, Depends(Stub(FileServiceInterface))],
) -> Any:
    file = await file_service.get_file(file_uuid=file_uuid)
    return file


@router.patch(
    '/files/{file_uuid}',
    response_model=FileOut,
    status_code=200,
)
async def update_file_status(
        file_uuid: UUID,
        file_service: Annotated[FileServiceInterface, Depends(Stub(FileServiceInterface))],
        status: Annotated[Literal['failed', 'success', 'in_process'], Body()],
) -> Any:
    file = await file_service.update_file_status(file_uuid=file_uuid, status=status)
    return file


@router.post(
    '/files',
    response_model=FileOut,
    status_code=201,
)
async def create_file(
        file: FileIn,
        file_service: Annotated[FileServiceInterface, Depends(Stub(FileServiceInterface))],
) -> Any:
    file = await file_service.create_file(data=file.data)
    return file
