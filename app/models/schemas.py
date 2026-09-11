from enum import Enum

from pydantic import BaseModel, Field


class ItemStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=500)
    status: ItemStatus = ItemStatus.ACTIVE


class Item(ItemCreate):
    id: int


class ItemListResponse(BaseModel):
    items: list[Item]
    dependency: dict | None
    dependency_error: str | None
