from dataclasses import dataclass


@dataclass
class ItemEntity:
    id: int
    name: str
    price: float
    deleted: bool = False


@dataclass
class DataItem:
    name: str
    price: float
    deleted: bool = False

    def to_entity(self, id: int) -> ItemEntity:
        return ItemEntity(
            id=id,
            name=self.name,
            price=self.price,
            deleted=self.deleted
        )


@dataclass
class DataItemPatch:
    name: str | None
    price: float | None

    def to_entity(self, entity: ItemEntity) -> ItemEntity:
        return ItemEntity(
            id=entity.id,
            name=self.name if self.name else entity.name,
            price=self.price if self.price else entity.price,
            deleted=entity.deleted
        )


@dataclass
class CartItem:
    id: int
    name: str
    quantity: int
    available: bool = True


@dataclass
class CartList:
    id: int
    items: list[CartItem]
    price: float
