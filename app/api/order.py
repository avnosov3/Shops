from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, paginate
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
    OrderStatusUpdate,
    OrderUpdateDBSchema,
    OrderUpdateSchema,
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
    await validators.check_rights_to_create_and_update_delete_obj(
        customer,
        await worker_crud.get_by_attribute(
            'phone_number', phone_number, session
        )
    )
    shopping_point_id = customer.shopping_point_id
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
        customer=customer.name,
        worker=worker.name,
        shopping_point=shopping_point.name
    )


@order_router.get('/', response_model=Page[OrderResponseSchema])
async def get_orders(
    customer: str | None = None,
    worker: str | None = None,
    shopping_point: str | None = None,
    status: str | None = None,
    session: AsyncSession = Depends(get_async_session)
):
    return paginate(await order_crud.get_all_with_names(
        session,
        customer,
        worker,
        shopping_point,
        status
    ))


@order_router.get('/{order_id}', response_model=OrderResponseSchema)
async def get_order(
    order_id: int,

    session: AsyncSession = Depends(get_async_session)
):
    order_db = await order_crud.get_with_names(order_id, session)
    if order_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=constants.ORDER_NOT_FOUND
        )


async def proccess_update_delete_permissions_and_obj_exsisting(phone_number, order_id, session):
    customer = await customer_crud.get_by_attribute(
        'phone_number', phone_number, session
    )
    await validators.check_rights_to_create_and_update_delete_obj(
        customer,
        await worker_crud.get_by_attribute(
            'phone_number', phone_number, session
        )
    )
    order_db = await validators.check_obj_exists(order_id, order_crud, constants.ORDER_NOT_FOUND, session)
    await validators.check_owner(order_db.customer_id, customer.id)
    return customer, order_db


@order_router.patch('/{order_id}', response_model=OrderResponseSchema)
async def update_order(
    phone_number: str,
    order_id: int,
    order_in: OrderUpdateSchema,
    session: AsyncSession = Depends(get_async_session)
):
    _, order_db = await proccess_update_delete_permissions_and_obj_exsisting(phone_number, order_id, session)
    order_update_schema = OrderUpdateDBSchema(
        close_date=order_in.close_date,
        status=order_in.status
    )
    worker_phone_number = order_in.worker_phone_number
    if order_in.worker_phone_number:
        worker = await worker_crud.get_by_attribute(
            'phone_number', worker_phone_number, session
        )
        if worker is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=constants.WORKER_NOT_FOUND
            )
        order_update_schema.worker_id = worker.id
        order_update_schema.shopping_point_id = worker.shopping_point_id
    await order_crud.update(
        order_db,
        order_update_schema,
        session
    )
    return await order_crud.get_with_names(order_id, session)


@order_router.delete('/{order_id}')
async def delete_order(
    phone_number: str,
    order_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    _, order_db = await proccess_update_delete_permissions_and_obj_exsisting(phone_number, order_id, session)
    await order_crud.delete(order_db, session)
    return dict(detail=constants.ORDER_DELETED)


@order_router.patch('/status/{order_id}')
async def update_status(
    phone_number: str,
    order_id: int,
    order_in: OrderStatusUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    _, order_db = await proccess_update_delete_permissions_and_obj_exsisting(phone_number, order_id, session)
    await order_crud.update(order_db, order_in, session)
    return await order_crud.get_with_names(order_id, session)
