from datetime import timedelta

from faker import Faker
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.models.customer import Customer
from app.models.order import Order, Status
from app.models.shopping_point import ShoppingPoint
from app.models.visit import Visit
from app.models.worker import Worker

autogenerate_router = APIRouter()
fake = Faker()


@autogenerate_router.get('/')
async def generate_shopping_points(session: AsyncSession = Depends(get_async_session)):
    shopping_points_amount = 100
    persons_amount = 200
    orders_amount = 250
    session.add_all([
        ShoppingPoint(name=fake.company()) for _ in range(shopping_points_amount)
    ])
    await session.commit()
    for model in (Worker, Customer):
        session.add_all([
            model(
                name=fake.name(),
                phone_number=fake.phone_number(),
                shopping_point_id=fake.random_int(min=1, max=shopping_points_amount)
            ) for _ in range(persons_amount)
        ])
    await session.commit()
    for _ in range(orders_amount):
        create_date = fake.date_time_between(start_date='-1y', end_date='now')
        session.add(Order(
            create_date=create_date,
            close_date=fake.date_time_between(
                start_date=create_date, end_date=create_date + timedelta(days=fake.random_int(min=1, max=30))
            ),
            status=fake.random_element(elements=Status).value,
            shopping_point_id=fake.random_int(min=1, max=shopping_points_amount),
            customer_id=fake.random_int(min=1, max=persons_amount),
            worker_id=fake.random_int(min=1, max=persons_amount),
        ))
    await session.commit()
    session.add_all([
        Visit(
            create_date=fake.date_time_between(start_date='-1y', end_date='now'),
            order_id=fake.random_int(min=1, max=orders_amount),
            shopping_point_id=fake.random_int(min=1, max=shopping_points_amount),
            customer_id=fake.random_int(min=1, max=persons_amount),
            worker_id=fake.random_int(min=1, max=persons_amount),
        ) for _ in range(orders_amount)
    ])
    await session.commit()
    return dict(detail='Data was generated')
