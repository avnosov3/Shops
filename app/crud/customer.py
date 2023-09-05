from app.crud.base import CRUDBase
from app.models.customer import Customer


class CustomerCRUD(CRUDBase):
    pass


customer_crud = CustomerCRUD(Customer)
