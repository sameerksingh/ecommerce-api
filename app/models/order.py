from datetime import datetime
from pydantic import BaseModel, Field
from typing import List


class ProductInOrder(BaseModel):
    name: str
    price: float
    quantity: int
    id: str


class Order(BaseModel):
    user_id: str
    timestamp: datetime
    status: str = Field(choices=["Initiated", "Delivering", "Delivered"], default="Initiated")
    bill: float
    products: List[ProductInOrder]
