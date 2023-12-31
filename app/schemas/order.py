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
    status: Status
    customer: str
    worker: str
    shopping_point: str

    class Config:
        orm_mode = True


class OrderUpdateSchema(BaseModel):
    close_date: datetime | None = Field(None, example=TO_TIME)
    status: Status | None = None
    worker_phone_number: str | None = None


class OrderUpdateDBSchema(BaseModel):
    close_date: datetime | None = Field(None, example=TO_TIME)
    status: Status | None = None
    worker_id: int | None = None
    shopping_point_id: int | None = None


class OrderStatusUpdate(BaseModel):
    status: Status
