from http import HTTPStatus
from http.client import HTTPException
from typing import Annotated

from fastapi import APIRouter, Query, Response
from pydantic import NonNegativeInt, PositiveInt, PositiveFloat, StrictBool, NonNegativeFloat

from lecture_2.hw.shop_api.contracts import (
    ItemResponse,
    ItemRequest,
    ItemRequestPatch,
)
from lecture_2.hw import shop_db

router_item = APIRouter(prefix="/item")


@router_item.get(
    "/{id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully returned requested item",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to return requested item as one was not found",
        },
    },
)
async def get_item_by_id(id: int):
    entity = shop_db.get_one_item(id)

    if entity.deleted:
        return Response(status_code=HTTPStatus.NOT_FOUND)

    if not entity:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            f"Request resource /item/{id} was not found",
        )

    return ItemResponse.from_entity(entity)


@router_item.get("/")
async def get_item_list(
        offset: Annotated[NonNegativeInt, Query()] = 0,
        limit: Annotated[PositiveInt, Query()] = 10,
        min_price: Annotated[NonNegativeFloat, Query()] = None,
        max_price: Annotated[PositiveFloat, Query()] = None,
        show_deleted: Annotated[bool, Query()] = False
) -> list[ItemResponse]:
    return [ItemResponse.from_entity(e) for e in
            shop_db.get_many_item(shop_db.FilterItem(min_price, max_price, show_deleted), offset, limit)]


@router_item.post(
    "/",
    status_code=HTTPStatus.CREATED,
)
async def post_item(info: ItemRequest, response: Response) -> ItemResponse:
    entity = shop_db.add_item(info.as_item_data())

    response.headers["location"] = f"/item/{entity.id}"

    return ItemResponse.from_entity(entity)


@router_item.delete("/{id}")
async def delete_pokemon(id: int) -> Response:
    shop_db.delete_item(id)
    return Response("Success delete")


@router_item.put(
    "/{id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully updated item",
        },
        HTTPStatus.NOT_MODIFIED: {
            "description": "Failed to modify item as one was not found",
        },
    }
)
async def put_item(
        id: int,
        info: ItemRequest,
) -> ItemResponse:
    entity = shop_db.update_item(id, info.as_item_data())

    if entity is None:
        raise HTTPException(
            HTTPStatus.NOT_MODIFIED,
            f"Requested resource /item/{id} was not found",
        )

    return ItemResponse.from_entity(entity)


@router_item.patch(
    "/{id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully updated pokemon",
        },
        HTTPStatus.NOT_MODIFIED: {
            "description": "Failed to modify pokemon as one was not found",
        },
    }
)
async def patch_item(
        response: Response,
        id: int,
        request: ItemRequestPatch,
) -> ItemResponse:
    entity = shop_db.patch_item(id, request.as_item_data())

    if not entity:
        raise HTTPException(
            HTTPStatus.NOT_MODIFIED,
            f"Requested resource /item/{id} was not found",
        )

    if entity.deleted:
        response.status_code = HTTPStatus.NOT_MODIFIED
        response.body = f"Requested resource /item/{id} was not found"

    return ItemResponse.from_entity(entity)
