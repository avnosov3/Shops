from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.core.db import Base
from app.models import constants


class ShoppingPoint(Base):
    name = Column(String(constants.MAX_LENGHT), nullable=False)

    customers = relationship('Customer', cascade='delete')
    workers = relationship('Worker', cascade='delete')
    orders = relationship('Order', cascade='delete')
    visits = relationship('Visit', cascade='delete')
