from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.core.db import Base
from app.models import constants


class ShoppingPoint(Base):
    name = Column(String(constants.MAX_LENGHT), nullable=False)
    # Создаем связь с таблицей Customer
    customers = relationship('Customer', back_populates='shopping_point')

    # Создаем связь с таблицей Worker
    workers = relationship('Worker', back_populates='shopping_point')
