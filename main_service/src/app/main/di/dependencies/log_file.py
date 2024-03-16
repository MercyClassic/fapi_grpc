from app.application.services.log_file import LogFileService


def get_log_file_service(channel_addr: str) -> LogFileService:
    return LogFileService(channel_addr)
