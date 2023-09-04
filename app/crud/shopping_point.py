from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.customer import Customer
from app.models.shopping_point import ShoppingPoint
from app.models.worker import Worker


class ShoppingPointCRUD(CRUDBase):

    async def get_by_phone_number(self, phone_number: str, session: AsyncSession):
        return await session.scalar(
            select(ShoppingPoint).join(Worker).where(Worker.phone_number == phone_number)
        ) or await session.scalar(
            select(ShoppingPoint).join(Customer).where(Customer.phone_number == phone_number)
        )


shopping_point_crud = ShoppingPointCRUD(ShoppingPoint)
