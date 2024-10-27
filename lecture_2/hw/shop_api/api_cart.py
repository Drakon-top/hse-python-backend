from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from typing import Annotated
from fastapi import APIRouter, Query, Response
from pydantic import NonNegativeInt, PositiveInt, PositiveFloat, StrictBool, NonNegativeFloat
from lecture_2.hw.shop_api.contracts import (
    ItemResponse,
    ItemRequestPatch,
)
from lecture_2.hw.shop_db.models import (
    CartList,
    CartItem,
)
from lecture_2.hw import shop_db

router_cart = APIRouter(prefix="/cart")


@router_cart.post(
    "/",
    status_code=HTTPStatus.CREATED,
)
async def post_cart(response: Response) -> CartList:
    entity = shop_db.add_cart()

    response.headers["location"] = f"/cart/{entity.id}"

    return entity


@router_cart.get(
    "/{id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully returned requested item",
        },
    },
)
async def get_cart_by_id(id: int):
    entity = shop_db.get_one_cart(id)

    if not entity:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            f"Request resource /item/{id} was not found",
        )

    return entity


@router_cart.get("/")
async def get_item_list(
        offset: Annotated[NonNegativeInt, Query()] = 0,
        limit: Annotated[PositiveInt, Query()] = 10,
        min_price: Annotated[NonNegativeFloat, Query()] = None,
        max_price: Annotated[PositiveFloat, Query()] = None,
        min_quantity: Annotated[NonNegativeInt, Query()] = None,
        max_quantity: Annotated[NonNegativeInt, Query()] = None,
) -> list[CartList]:
    print(max_quantity)
    return [e for e in shop_db.get_many_cart(shop_db.FilterCart(min_price, max_price, min_quantity, max_quantity), offset, limit)]


@router_cart.post(
    "/{cart_id}/add/{item_id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully returned requested item",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to return requested item as one was not found",
        },
    },
)
async def post_cart(cart_id: int, item_id: int):
    res = shop_db.add_list(cart_id, item_id)

    if not res:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            f"Request resource /item/{id} was not found",
        )

    return res