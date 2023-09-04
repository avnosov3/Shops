from enum import Enum

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as EnumSQL

from app.models.visti_order_base import VisitOrderBase


class Status(str, Enum):
    STARTED = 'started'
    ENDED = 'ended'
    IN_PROCCES = 'in process'
    AWAITING = 'awaiting'
    CANCELED = 'canceled'


class Order(VisitOrderBase):
    close_date = Column(DateTime)
    status = Column(EnumSQL(
        Status, name='status',
        values_callable=lambda statuses: [status.value for status in statuses]
    ))

    visit = relationship('Visit', uselist=False, cascade='delete')
