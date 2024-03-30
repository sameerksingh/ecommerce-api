from pydantic import BaseModel
from typing import List
from app.models.product import ProductInCart


class Cart(BaseModel):
    user_id: str | None = None
    products: List[ProductInCart] = []
