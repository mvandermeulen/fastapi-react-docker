from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel
from sqlmodel import Field


def fix_uuid() -> UUID:
    # Note: Work around UUIDs with leading zeros: https://github.com/tiangolo/sqlmodel/issues/25
    # by making sure uuid str does not start with a leading 0
    val = uuid4()
    while val.hex[0] == '0':
        val = uuid4()

    return val


class IDModelMixin(BaseModel):
    id: Optional[UUID] = Field(
        default_factory=fix_uuid,
        primary_key=True,
        index=True,
        nullable=False,
    )


class IDRead(BaseModel):
    id: UUID
