import os

from app.application.interfaces.services.log import LogFileServiceInterface
from app.application.interfaces.services.main_file import MainFileServiceInterface
from app.application.services.log import LogFileService
from app.application.services.main_file import MainFileService
from dishka import Provider, Scope, provide


class LogServiceProvider(Provider):
    scope = Scope.REQUEST

    @provide()
    def get_main_file_service_gateway(self) -> MainFileServiceInterface:
        return MainFileService(main_file_service_addr=os.environ['MAIN_FILE_SERVICE_ADDR'])

    @provide()
    def get_log_file_service(
            self,
            main_file_service: MainFileServiceInterface,
    ) -> LogFileServiceInterface:
        return LogFileService(main_file_service=main_file_service)
