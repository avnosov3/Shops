# from sqlalchemy import Column, Integer, ForeignKey

from app.models.person_base import PersonBase


class Customer(PersonBase):
    # shopping_point_id = Column(Integer, ForeignKey('shoppingpoint.id'))
    pass
