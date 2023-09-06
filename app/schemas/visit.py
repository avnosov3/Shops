from datetime import datetime

from pydantic import BaseModel


class VisitCreateSchema(BaseModel):
    worker_phone_number: str


class VisitCreateDBSchema(BaseModel):
    worker_id: int
    order_id: int
    customer_id: int
    shopping_point_id: int


class VisitResponseSchema(BaseModel):
    create_date: datetime
    order_id: int
    worker: str
    customer: str
    shopping_point: str

    class Config:
        orm_mode = True
