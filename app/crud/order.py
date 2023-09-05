from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models.customer import Customer
from app.models.order import Order
from app.models.shopping_point import ShoppingPoint
from app.models.worker import Worker


class OrderCRUD(CRUDBase):

    async def get_all_with_names(self, session):
        orders = await session.execute(
            select(
                Order.id,
                Order.status,
                Order.close_date,
                Order.create_date,
                Customer.name.label('customer'),
                Worker.name.label('worker'),
                ShoppingPoint.name.label('shopping_point')
            )
            .join(Customer, Order.customer_id == Customer.id)
            .join(Worker, Order.worker_id == Worker.id)
            .join(ShoppingPoint, Order.shopping_point_id == ShoppingPoint.id)
        )
        return orders.fetchall()

    async def get_with_names(self, order_id, session):
        orders = await session.execute(
            select(
                Order.id,
                Order.status,
                Order.close_date,
                Order.create_date,
                Customer.name.label('customer'),
                Worker.name.label('worker'),
                ShoppingPoint.name.label('shopping_point')
            )
            .join(Customer, Order.customer_id == Customer.id)
            .join(Worker, Order.worker_id == Worker.id)
            .join(ShoppingPoint, Order.shopping_point_id == ShoppingPoint.id)
            .where(Order.id == order_id)
        )
        return orders.fetchone()


order_crud = OrderCRUD(Order)
