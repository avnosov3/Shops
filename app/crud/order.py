from app.crud.base import CRUDBase
from app.models.order import Order


class OrderCRUD(CRUDBase):
    pass


order_crud = OrderCRUD(Order)
