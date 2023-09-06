from fastapi import FastAPI
from fastapi_pagination import add_pagination
from sqladmin import Admin

from app.admin.panel import (
    CustomerAdmin,
    OrderAdmin,
    ShoppingPointAdmin,
    VisittAdmin,
    WorkerAdmin,
)
from app.api.routers import main_router_v1
from app.core.db import engine

app = FastAPI()

app.include_router(main_router_v1)

add_pagination(app)

admin = Admin(app, engine)

admin.add_view(CustomerAdmin)
admin.add_view(WorkerAdmin)
admin.add_view(ShoppingPointAdmin)
admin.add_view(OrderAdmin)
admin.add_view(VisittAdmin)
