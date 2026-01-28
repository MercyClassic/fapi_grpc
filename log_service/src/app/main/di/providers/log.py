import os

from dishka import Provider, Scope, provide

from app.application.services.log import LogFileService, LogFileServiceInterface
from app.application.services.main_file import MainFileService, MainFileServiceInterface


class LogServiceProvider(Provider):
    scope = Scope.REQUEST

    @provide()
    def get_main_file_service_gateway(self) -> MainFileServiceInterface:
        return MainFileService(
            main_file_service_addr=os.environ['MAIN_FILE_SERVICE_ADDR']
        )

    @provide()
    def get_log_file_service(
        self,
        main_file_service: MainFileServiceInterface,
    ) -> LogFileServiceInterface:
        return LogFileService(main_file_service=main_file_service)
