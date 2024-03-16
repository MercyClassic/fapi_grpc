from typing import TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

DATA_EXAMPLE = Field(examples=[{'some_key': 'some_value'}])
INPUT_DATA = TypeVar('INPUT_DATA')


class FileIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    data: dict = DATA_EXAMPLE

    @field_validator('data')
    def validate_data(cls, value: INPUT_DATA) -> INPUT_DATA:
        if value == {}:
            raise ValueError("Data can't be empty")
        return value


class FileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    uuid: UUID
    status: str
    data: dict | None = DATA_EXAMPLE
