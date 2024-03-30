# app/views/cart_views.py
from fastapi import APIRouter, Depends
from app.controllers.cart_controller import CartController
from app.models.cart import Cart
from utils import HTTPResponse, verify_token, has_role

router = APIRouter(tags=["cart"])


@router.get('/api/carts/{user_id}')
@has_role(["Admin", "Customer"])
async def get_cart(user_id: str, role: str = Depends(verify_token)):
    cart = CartController.get_cart_by_user_id(user_id)
    if cart:
        return HTTPResponse(cart, 200)
    return HTTPResponse({"message": "Cart not found"}, 404)


@router.patch('/api/carts')
@has_role(["Admin", "Customer"])
async def update_user_cart(cart: Cart | None = None, user_id: str | None = None, product_id: str | None = None, quantity: int = 1, role: str = Depends(verify_token)):
    try:
        if quantity==0:
            return CartController.get_cart_by_user_id(user_id)
        elif product_id:
            updated_cart = CartController.insert_product_in_cart(user_id, product_id, quantity)
        else:
            if not cart.user_id:
                cart.user_id = user_id
            updated_cart = CartController.update_cart(cart)
        return HTTPResponse(updated_cart, 200)
    except Exception as e:
        return HTTPResponse({"message": str(e)}, 404)


@router.put('/api/carts/{user_id}')
@has_role(["Admin", "Customer"])
async def clear_cart(user_id: str, role: str = Depends(verify_token)):
    updated_cart = CartController.update_cart(Cart(user_id=user_id, products=[]))
    return HTTPResponse(updated_cart, 200)

