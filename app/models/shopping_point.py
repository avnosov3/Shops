from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.core.db import Base
from app.models import constants


class ShoppingPoint(Base):
    name = Column(String(constants.MAX_LENGHT), nullable=False)

    customers = relationship('Customer', cascade='delete', back_populates='shopping_point')
    workers = relationship('Worker', cascade='delete', back_populates='shopping_point')
    orders = relationship('Order', cascade='delete', back_populates='shopping_point')
    visits = relationship('Visit', cascade='delete', back_populates='shopping_point')
