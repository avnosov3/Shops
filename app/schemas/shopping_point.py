from pydantic import BaseModel


class ShoppingPointResponseDBSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
