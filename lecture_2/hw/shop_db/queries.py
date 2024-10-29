from typing import Iterable
from dataclasses import dataclass

from .models import (
    ItemEntity,
    CartItem,
    CartList,
    DataItem,
    DataItemPatch,
)


@dataclass
class FilterItem:
    min_price: float = 0.0
    max_price: float = -1
    show_deleted: bool = False

    def __init__(self, min_price, max_price, show_deleted):
        if min_price is not None:
            self.min_price = min_price

        if max_price is not None:
            self.max_price = max_price

        self.show_deleted = show_deleted

    def filter(self, item: ItemEntity) -> bool:
        return self.min_price <= item.price and (
                self.max_price >= item.price or self.max_price == -1) and (
                self.show_deleted or not item.deleted)


@dataclass
class FilterCart:
    min_price: float = 0.0
    max_price: float = -1
    min_quantity: int = 0
    max_quantity: int = -1

    def __init__(self, min_price, max_price, min_quantity, max_quantity):
        if min_price is not None:
            self.min_price = min_price

        if max_price is not None:
            self.max_price = max_price

        if min_quantity is not None:
            self.min_quantity = min_quantity

        if max_quantity is not None:
            self.max_quantity = max_quantity

    def filter(self, item: CartList) -> bool:
        count = sum([i.quantity for i in item.items])
        return self.min_price <= item.price and (
                self.max_price >= item.price or self.max_price == -1) and (
                self.max_quantity >= count or self.max_quantity == -1) and (
                count >= self.min_quantity)


_data_item = dict[int, ItemEntity]()
_data_cart = dict[int, CartList]()


def int_id_generator() -> Iterable[int]:
    i = 0
    while True:
        yield i
        i += 1


_id_item_generator = int_id_generator()
_id_cart_generator = int_id_generator()


def get_many_item(
        filterItem: FilterItem,
        offset: int = 0,
        limit: int = 10,
) -> Iterable[ItemEntity]:
    curr = 0
    for entity in _data_item.values():
        if not filterItem.filter(entity):
            continue

        if offset <= curr < offset + limit:
            yield entity

        curr += 1


def get_many_cart(
        filterCart: FilterCart,
        offset: int = 0,
        limit: int = 10,
) -> Iterable[CartList]:
    curr = 0
    for entity in _data_cart.values():
        if not filterCart.filter(entity):
            continue

        if offset <= curr < offset + limit:
            yield entity

        curr += 1


def add_item(data: DataItem) -> ItemEntity:
    id = next(_id_item_generator)
    item = data.to_entity(id)
    _data_item[id] = item

    return item


def add_cart() -> CartList:
    id = next(_id_cart_generator)
    item = CartList(id=id, items=list(), price=0.0)
    _data_cart[id] = item

    return item


def get_one_item(id: int) -> ItemEntity | None:
    if id not in _data_item:
        return None

    return _data_item[id]


def get_one_cart(id: int) -> CartList | None:
    print(_data_cart)
    if id not in _data_cart:
        return None

    return _data_cart[id]


def delete_item(id: int) -> bool:
    if id not in _data_item:
        return False

    _data_item[id].deleted = True
    return True


def update_item(id: int, data: DataItem) -> ItemEntity | None:
    if id not in _data_item:
        return None

    entity = data.to_entity(id)
    _data_item[id] = entity

    return entity


def patch_item(id: int, data: DataItemPatch) -> ItemEntity | None:
    if id not in _data_item:
        return None

    entity = data.to_entity(_data_item[id])
    _data_item[id] = entity

    return entity


def add_list(cart_id, item_id) -> CartList | None:
    cart = _data_cart[cart_id]
    item = _data_item[item_id]

    if cart is None or item is None:
        return None
    ids = [i.id for i in cart.items]
    if item_id in ids:
        for i in cart.items:
            if i.id == item_id:
                i.quantity += 1
                break
    else:
        cart.items.append(CartItem(id=item.id, name=item.name, quantity=1))
    cart.price += item.price
    return cart
