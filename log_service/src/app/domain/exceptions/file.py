from app.domain.exceptions.base import DomainException


class FileNotFound(DomainException):
    def __init__(self):
        super().__init__('File not found')
