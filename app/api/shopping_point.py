from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.shopping_point import shopping_point_crud
from app.schemas.shopping_point import ShoppingPointResponseDBSchema

shopping_point_router = APIRouter()


@shopping_point_router.get('/', response_model=ShoppingPointResponseDBSchema)
async def get_shopping_point(
    phone_number: str,
    session: AsyncSession = Depends(get_async_session)
):
    return await shopping_point_crud.get_all_by_phone_number(
        phone_number, session
    )
