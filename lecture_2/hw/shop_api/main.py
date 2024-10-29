from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from lecture_2.hw.shop_api.api_cart import router_cart
from lecture_2.hw.shop_api.api_item import router_item

app = FastAPI(title="Shop API")
Instrumentator().instrument(app).expose(app)

app.include_router(router_cart)
app.include_router(router_item)
