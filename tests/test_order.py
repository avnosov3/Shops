from datetime import datetime, timedelta

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer
from app.models.order import Order
from app.models.shopping_point import ShoppingPoint
from app.models.worker import Worker

TO_TIME = (
    datetime.now() + timedelta(hours=1)
)


async def create_order(session: AsyncSession):
    shopping_point = ShoppingPoint(name='test shopping point name')
    session.add(shopping_point)
    await session.commit()
    shopping_point_id = shopping_point.id
    customer = Customer(name='test customer name', phone_number='+7333', shopping_point_id=shopping_point_id)
    session.add(customer)
    await session.commit()
    worker = Worker(name='test worker name', phone_number='+7111', shopping_point_id=shopping_point_id)
    session.add(worker)
    await session.commit()
    order = Order(
        close_date=TO_TIME,
        shopping_point_id=shopping_point_id,
        status='started',
        customer_id=customer.id,
        worker_id=worker.id
    )
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order, shopping_point, customer, worker


async def test_read_order(client: TestClient, session: AsyncSession) -> None:
    order, shopping_point, customer, worker = await create_order(session)
    order_id = str(order.id)
    response = client.get(f'/api/v1/order/{order_id}')
    data = response.json()
    assert response.status_code == 200
    for value, expected in (
        (data['create_date'], order.create_date.strftime('%Y-%m-%dT%H:%M:%S.%f')),
        (data['close_date'], order.close_date.strftime('%Y-%m-%dT%H:%M:%S.%f')),
        (data['shopping_point'], shopping_point.name),
        (data['status'], order.status),
        (data['customer'], customer.name),
        (data['worker'], worker.name),
    ):
        assert value == expected
