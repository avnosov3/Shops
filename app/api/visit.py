from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import constants, validators
from app.core.db import get_async_session
from app.crud.customer import customer_crud
from app.crud.order import order_crud
from app.crud.shopping_point import shopping_point_crud
from app.crud.visit import visit_crud
from app.crud.worker import worker_crud
from app.schemas.visit import (
    VisitCreateDBSchema,
    VisitCreateSchema,
    VisitResponseSchema,
)

visit_router = APIRouter()


@visit_router.post('/{order_id}')
async def create_visit(
    order_id: int,
    phone_number: str,
    visit_in: VisitCreateSchema,
    session: AsyncSession = Depends(get_async_session)
):
    order_db = await validators.check_obj_exists(order_id, order_crud, constants.ORDER_NOT_FOUND, session)
    customer = await customer_crud.get_by_attribute(
        'phone_number', phone_number, session
    )
    shopping_point_id = customer.shopping_point_id
    worker = await worker_crud.get_by_attribute(
        'phone_number', visit_in.worker_phone_number, session
    )
    if worker is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=constants.WORKER_NOT_FOUND
        )
    await validators.check_rights_to_create_and_update_delete_obj(
        customer,
        worker
    )
    await validators.check_deadline(order_db.close_date)
    await validators.check_order_in_visit(visit_crud, order_id, session)
    worker = await worker_crud.get_by_attribute(
        'phone_number', visit_in.worker_phone_number, session
    )
    await validators.check_order_belongs_to_worker(order_db.worker_id, worker.id)
    visit_db = await visit_crud.create(
        VisitCreateDBSchema(
            order_id=order_id,
            customer_id=customer.id,
            shopping_point_id=customer.shopping_point_id,
            worker_id=worker.id
        ),
        session
    )
    shopping_point = await shopping_point_crud.get(shopping_point_id, session)
    return VisitResponseSchema(
        create_date=visit_db.create_date,
        order_id=order_id,
        worker=worker.name,
        customer=customer.name,
        shopping_point=shopping_point.name
    )


@visit_router.get('/', response_model=Page[VisitResponseSchema])
async def get_visits(
    customer: str | None = None,
    worker: str | None = None,
    shopping_point: str | None = None,
    session: AsyncSession = Depends(get_async_session)
):
    return paginate(await visit_crud.get_all_with_names(
        session,
        customer,
        worker,
        shopping_point,
    ))


@visit_router.get('/{visit_id}', response_model=VisitResponseSchema)
async def get_visit(
    visit_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    visit_db = await visit_crud.get_with_names(visit_id, session)
    if visit_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=constants.VISIT_NOT_FOUND
        )


@visit_router.patch('/{order_id}/{visit_id}')
async def update_visit(
    order_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    pass
