from sqlalchemy import Column, ForeignKey, Integer, String

from app.core.db import Base
from app.models import constants


class PersonBase(Base):
    __abstract__ = True

    name = Column(String(constants.MAX_LENGHT), nullable=False)
    phone_number = Column(String(constants.MAX_LENGHT), nullable=False)
    shopping_point_id = Column(Integer, ForeignKey('shopping_point.id'))

    OUT = 'Название "{}". Номер телефона "{}"'

    def __repr__(self):
        return self.OUT.format(self.name, self.phone_number)
