from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import constants
from app.core.db import get_async_session
from app.crud.shopping_point import shopping_point_crud
from app.schemas.shopping_point import ShoppingPointResponseDBSchema

shopping_point_router = APIRouter()


@shopping_point_router.get('/', response_model=ShoppingPointResponseDBSchema)
async def get_shopping_point(
    phone_number: str,
    session: AsyncSession = Depends(get_async_session)
):
    shopping_point = await shopping_point_crud.get_by_phone_number(
        phone_number, session
    )
    if shopping_point is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=constants.SHOPPING_POINT_NOT_FOUND.format(phone_number)
        )
    return shopping_point
