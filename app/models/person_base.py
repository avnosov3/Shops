from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from app.core.db import Base
from app.models import constants


class PersonBase(Base):
    __abstract__ = True

    name = Column(String(constants.MAX_LENGHT), nullable=False)
    phone_number = Column(String(constants.MAX_LENGHT), nullable=False)

    @declared_attr
    def shopping_point_id(cls):
        return Column(Integer, ForeignKey('shoppingpoint.id'), nullable=False)

    @declared_attr
    def visits(cls):
        return relationship('Visit', cascade='delete', back_populates='customer')

    @declared_attr
    def orders(cls):
        return relationship('Order', cascade='delete', back_populates='customer')

    OUT = 'Название "{}". Номер телефона "{}". Тороговая точка "{}"'

    def __repr__(self):
        return self.OUT.format(self.name, self.phone_number, self.shopping_point_id)
