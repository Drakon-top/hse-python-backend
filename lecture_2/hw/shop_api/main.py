from fastapi import FastAPI
from lecture_2.hw.shop_api.api_cart import router_cart
from lecture_2.hw.shop_api.api_item import router_item

app = FastAPI(title="Shop API")

app.include_router(router_cart)
app.include_router(router_item)
