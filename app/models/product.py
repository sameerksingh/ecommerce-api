from pydantic import BaseModel


class ProductUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    inventory: int | None = None


class ProductWithoutId(BaseModel):
    name: str
    price: float
    inventory: int


class Product(ProductWithoutId):
    id: str
