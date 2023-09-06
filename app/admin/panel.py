from sqladmin import ModelView

from app.models.customer import Customer
from app.models.order import Order
from app.models.shopping_point import ShoppingPoint
from app.models.visit import Visit
from app.models.worker import Worker


class CustomerAdmin(ModelView, model=Customer):
    column_list = [Customer.id, Customer.name, Customer.phone_number]
    column_searchable_list = [Customer.name, Customer.phone_number]


class WorkerAdmin(ModelView, model=Worker):
    column_list = [Worker.id, Worker.name, Worker.phone_number]
    column_searchable_list = [Worker.name, Worker.phone_number]


class ShoppingPointAdmin(ModelView, model=ShoppingPoint):
    column_list = [ShoppingPoint.id, ShoppingPoint.name]
    column_searchable_list = [ShoppingPoint.name]


class OrderAdmin(ModelView, model=Order):
    column_list = [
        Order.id,
        Order.create_date,
        Order.close_date,
        Order.status,
        Order.shopping_point_id,
        Order.customer_id,
        Order.worker_id
    ]


class VisittAdmin(ModelView, model=Visit):
    column_list = [
        Visit.id,
        Visit.create_date,
        Visit.order_id,
        Order.customer_id,
        Order.worker_id,
        Order.shopping_point_id
    ]
