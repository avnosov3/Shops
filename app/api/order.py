from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import constants, validators
from app.core.db import get_async_session
from app.crud.customer import customer_crud
from app.crud.order import order_crud
from app.crud.shopping_point import shopping_point_crud
from app.crud.worker import worker_crud
from app.schemas.order import (
    OrderCreateDBSchema,
    OrderCreateSchema,
    OrderResponseSchema,
)

order_router = APIRouter()


@order_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_order(
    phone_number: str,
    order_in: OrderCreateSchema,
    session: AsyncSession = Depends(get_async_session)
):
    await validators.check_close_date(order_in.close_date)
    customer = await customer_crud.get_by_attribute(
        'phone_number', phone_number, session
    )
    shopping_point_id = customer.shopping_point_id
    await validators.check_rights_to_create_order(
        customer,
        await worker_crud.get_by_attribute(
            'phone_number', phone_number, session
        )
    )
    worker = await worker_crud.get_by_attribute(
        'shopping_point_id', shopping_point_id, session
    )
    if worker.shopping_point_id != shopping_point_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=constants.WORKER_NOT_BELOGNS
        )
    order_db = await order_crud.create(OrderCreateDBSchema(
        **order_in.dict(), shopping_point_id=shopping_point_id, customer_id=customer.id, worker_id=worker.id),
        session
    )
    shopping_point = await shopping_point_crud.get(shopping_point_id, session)
    return OrderResponseSchema(
        create_date=order_db.create_date,
        close_date=order_in.close_date,
        worker=worker.name,
        shopping_point=shopping_point.name
    )
