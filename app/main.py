from fastapi import FastAPI

from app.api.routers import main_router_v1

app = FastAPI()
app.include_router(main_router_v1)
