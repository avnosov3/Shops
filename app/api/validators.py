from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import constants


async def check_obj_exists(obj_id, crud, message, session: AsyncSession):
    db_obj = await crud.get(obj_id, session)
    if db_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message
        )
    return db_obj


async def check_rights_to_create_and_update_delete_obj(customer, fake_customer):
    if customer is None and fake_customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=constants.CUSTOMER_NOT_FOUND
        )
    if fake_customer and customer is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=constants.CREATE_UPDATE_OBJECT_FORBIDDEN
        )


async def check_close_date(close_date):
    if close_date <= datetime.now():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=constants.CLOSE_DATE_IN_PAST
        )


async def check_owner(order_customer_id, customer_id):
    if order_customer_id != customer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=constants.NOT_ORDER_OWNER
        )


async def check_deadline(close_date):
    if close_date <= datetime.now():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=constants.VISIT_CREATE_FORBIDDEN
        )


async def check_order_in_visit(crud, order_id, session):
    if await crud.get_by_attribute(
        'order_id', order_id, session
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=constants.ORDER_IN_VISIT_EXISTS
        )


async def check_order_belongs_to_worker(order_worker_id, worker_id, message=constants.WRONG_WORKER_IN_VISIT):
    if order_worker_id != worker_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message
        )
