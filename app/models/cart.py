from pydantic import BaseModel
from typing import List


class ProductInCart(BaseModel):
    quantity: int
    id: str


class Cart(BaseModel):
    user_id: str
    products: List[ProductInCart] = []
