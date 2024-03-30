from pydantic import BaseModel


class Product_update(BaseModel):
    name: str | None = None
    price: float | None = None

class Product_without_id(BaseModel):
    name: str
    price: float

class Product(BaseModel):
    name: str
    price: float
    id: str

class ProductInCart(BaseModel):
    quantity: int
    id: str
