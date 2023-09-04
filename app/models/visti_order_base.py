from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.ext.declarative import declared_attr

from app.core.db import Base


class VisitOrderBase(Base):
    __abstract__ = True

    create_date = Column(DateTime, default=datetime.utcnow)

    @declared_attr
    def shopping_point_id(cls):
        return Column(Integer, ForeignKey('shoppingpoint.id'), nullable=False)

    @declared_attr
    def customer_id(cls):
        return Column(Integer, ForeignKey('customer.id'), nullable=False)

    @declared_attr
    def worker_id(cls):
        return Column(Integer, ForeignKey('worker.id'), nullable=False)

    OUT = 'Заказчик "{}". Исполнитель "{}". Торговая точка "{}".'

    def __repr__(self):
        return self.OUT.format(self.customer_id, self.worker_id, self.shopping_point_id)
