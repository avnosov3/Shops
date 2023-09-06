from fastapi import APIRouter

from app.api.autogenerate import autogenerate_router
from app.api.order import order_router
from app.api.shopping_point import shopping_point_router
from app.api.visit import visit_router

main_router_v1 = APIRouter(prefix='/api/v1')
main_router_v1.include_router(autogenerate_router, prefix='/autogenerate', tags=['Autogenerate'])
main_router_v1.include_router(shopping_point_router, prefix='/shopping-point', tags=['ShoppingPoint'])
main_router_v1.include_router(order_router, prefix='/order', tags=['Order'])
main_router_v1.include_router(visit_router, prefix='/visit', tags=['Visit'])
