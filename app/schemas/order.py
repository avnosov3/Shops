from datetime import datetime, timedelta

from pydantic import BaseModel, Field

from app.models.order import Status

TO_TIME = (
    datetime.now() + timedelta(hours=1)
).isoformat(timespec='minutes')


class OrderCreateSchema(BaseModel):
    close_date: datetime = Field(..., example=TO_TIME)
    status: Status


class OrderCreateDBSchema(OrderCreateSchema):
    shopping_point_id: int
    customer_id: int
    worker_id: int


class OrderResponseSchema(BaseModel):
    create_date: datetime
    close_date: datetime
    worker: str
    shopping_point: str
