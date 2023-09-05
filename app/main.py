from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.api.routers import main_router_v1

app = FastAPI()
app.include_router(main_router_v1)
add_pagination(app)
