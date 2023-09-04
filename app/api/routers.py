from fastapi import APIRouter

from app.api.autogenerate import autogenerate_router

main_router_v1 = APIRouter()
main_router_v1.include_router(autogenerate_router, prefix='/autogenerate',
                              tags=['Autogenerate'])
