# app/views/order_views.py
from fastapi import APIRouter, Depends
from app.controllers.order_controller import OrderController
from app.controllers.cart_controller import CartController
from utils import HTTPResponse, verify_token, has_role
from app.models.cart import Cart


router = APIRouter(tags=["order"])


@router.get("/api/orders/")
@has_role(["Admin"])
async def get_orders(role: str = Depends(verify_token)):
    orders = OrderController.get_orders()
    orders = orders if orders else []
    return HTTPResponse(orders, 200)


@router.get("/api/orders/{user_id}")
@has_role(["Admin", "Customer"])
async def get_order_of_user(user_id: str, role: str = Depends(verify_token)):
    orders = OrderController.get_order_by_user_id(user_id)
    orders = orders if orders else []
    return HTTPResponse(orders, 200)


@router.put("/api/orders/place_order/{user_id}")
@has_role(["Admin", "Customer"])
async def place_order(user_id: str, role: str = Depends(verify_token)):
    order_details = OrderController.place_order(user_id)
    CartController.update_cart(Cart(user_id=user_id, products=[]))
    return HTTPResponse(order_details, 200)
