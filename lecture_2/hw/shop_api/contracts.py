from __future__ import annotations
from pydantic import BaseModel, ConfigDict
from typing import Optional

from lecture_2.hw.shop_db.models import (
    ItemEntity,
    CartItem,
    CartList,
    DataItem,
    DataItemPatch,
)


class ItemResponse(BaseModel):
    id: int
    name: str
    price: float

    @staticmethod
    def from_entity(entity: ItemEntity) -> ItemResponse:
        return ItemResponse(
            id=entity.id,
            name=entity.name,
            price=entity.price,
        )


class ItemRequest(BaseModel):
    name: str
    price: float
    show_deleted: bool = False

    def as_item_data(self) -> DataItem:
        return DataItem(
            name=self.name,
            price=self.price,
            deleted=self.show_deleted,
        )


class ItemRequestPatch(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None

    model_config = ConfigDict(extra="forbid")

    def as_item_data(self) -> DataItemPatch:
        return DataItemPatch(
            name=self.name,
            price=self.price,
        )
