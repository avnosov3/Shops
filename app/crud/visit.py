from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models.customer import Customer
from app.models.shopping_point import ShoppingPoint
from app.models.visit import Visit
from app.models.worker import Worker


class VisitCRUD(CRUDBase):

    async def get_all_with_names(
        self,
        session,
        customer_filter=None,
        worker_filter=None,
        shopping_point_filter=None,
    ):
        query = (select(
            Visit.id,
            Visit.create_date,
            Visit.order_id,
            Customer.name.label('customer'),
            Worker.name.label('worker'),
            ShoppingPoint.name.label('shopping_point')
        )
            .join(Customer, Visit.customer_id == Customer.id)
            .join(Worker, Visit.worker_id == Worker.id)
            .join(ShoppingPoint, Visit.shopping_point_id == ShoppingPoint.id)
        )
        if customer_filter:
            query = query.where(Customer.name == customer_filter)
        if worker_filter:
            query = query.where(Worker.name == worker_filter)
        if shopping_point_filter:
            query = query.where(ShoppingPoint.name == shopping_point_filter)
        orders = await session.execute(query)
        return orders.fetchall()

    async def get_with_names(self, visit_id, session):
        orders = await session.execute(
            select(
                Visit.id,
                Visit.create_date,
                Visit.order_id,
                Customer.name.label('customer'),
                Worker.name.label('worker'),
                ShoppingPoint.name.label('shopping_point')
            )
            .join(Customer, Visit.customer_id == Customer.id)
            .join(Worker, Visit.worker_id == Worker.id)
            .join(ShoppingPoint, Visit.shopping_point_id == ShoppingPoint.id)
            .where(Visit.id == visit_id)
        )
        return orders.fetchone()


visit_crud = VisitCRUD(Visit)
