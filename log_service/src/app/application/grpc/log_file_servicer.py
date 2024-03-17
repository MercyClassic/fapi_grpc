import json

from app.application.grpc import log_file_service_pb2, log_file_service_pb2_grpc
from app.application.interfaces.services.file import FileServiceInterface
from dishka import AsyncContainer

Response = log_file_service_pb2.Response


class LogFileServicer(log_file_service_pb2_grpc.LogFileServiceServicer):
    def __init__(self, container: AsyncContainer) -> None:
        self._container = container
        self._response_factory = Response

    async def get_file(self, request, context) -> Response:
        async with self._container() as request_container:
            file_service = await request_container.get(FileServiceInterface)
            file = await file_service.get_file(request.file_uuid)
            response = self._response_factory(file_uuid=file.uuid, data=json.dumps(file.data))
        return response

    async def create_file(self, request, context) -> Response:
        async with self._container() as request_container:
            file_service = await request_container.get(FileServiceInterface)
            file = await file_service.create_file(file_uuid=request.file_uuid, data=json.loads(request.data))
            response = self._response_factory(file_uuid=file.uuid, data=json.dumps(file.data))
        return response
