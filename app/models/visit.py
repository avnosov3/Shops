from sqlalchemy import Column, ForeignKey, Integer

from app.models.visti_order_base import VisitOrderBase


class Visit(VisitOrderBase):
    order_id = Column(Integer, ForeignKey('order.id'))
