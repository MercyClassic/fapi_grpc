from typing import Union
from uuid import UUID

from odmantic import Field, Model
from pydantic import field_validator


class File(Model):
    uuid: Union[UUID, str] = Field(primary_field=True, unique=True, index=True)
    data: dict

    @field_validator('uuid')
    def convert_uuid_to_str(cls, value: UUID) -> str:
        return str(value)

    model_config = {
        'collection': 'files',
    }
