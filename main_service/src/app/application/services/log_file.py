import json
from uuid import UUID

from app.application.grpc import log_file_service_pb2, log_file_service_pb2_grpc
from app.application.interfaces.services.log_file import LogFileServiceInterface

from grpc import aio


class LogFileService(LogFileServiceInterface):
    def __init__(self, channel_addr: str):
        self.channel_addr = channel_addr
        self._log_service_stub = log_file_service_pb2_grpc.LogFileServiceStub
        self._get_file_request_factory = log_file_service_pb2.GetFileRequest
        self._create_file_request_factory = log_file_service_pb2.CreateFileRequest

    async def get_file_data(self, file_uuid: UUID) -> dict[str, str | int | dict]:
        async with aio.insecure_channel(self.channel_addr) as channel:
            stub = self._log_service_stub(channel)
            request = self._get_file_request_factory(file_uuid=str(file_uuid))
            response = await stub.get_file(request)
        return json.loads(response.data)

    async def create_file(
            self,
            file_uuid: UUID,
            file_data: dict[str, str | int | dict],
    ) -> dict[str, str | int | dict]:
        async with aio.insecure_channel(self.channel_addr) as channel:
            stub = self._log_service_stub(channel)
            request = self._create_file_request_factory(
                file_uuid=str(file_uuid),
                data=json.dumps(file_data),
            )
            response = await stub.create_file(request)
        return json.loads(response.data)
