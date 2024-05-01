# app/views/user_views.py
from fastapi import APIRouter, Depends
from app.controllers.user_controller import UserController
from app.controllers.cart_controller import CartController
from app.models.user import User
from utils import HTTPResponse, verify_token, has_role, hash_password
from enum import Enum


# Define enum for options
class User_Fields(str, Enum):
    email = "email"
    id = "id"


router = APIRouter(tags=["user"])


@router.get('/api/users/{field}')
@has_role(["Admin", "Customer"])
async def get_user(field: str, by_email: User_Fields, role: str = Depends(verify_token)):
    if by_email == "email":
        user = UserController.get_user_by_email(field)
    else:
        user = UserController.get_user_by_id(field)
    if user:
        return HTTPResponse(user, 200)
    else:
        return HTTPResponse({"message": "User not found"}, 404)


@router.post('/api/users')
async def create_user_endpoint(user: User):
    user.password = hash_password(user.password, user.salt)
    new_user = UserController.create_user(user)
    if not new_user:
        return HTTPResponse({"message": "This username is already in use"}, 409)
    CartController.create_cart(new_user.id)
    return HTTPResponse(new_user, 201)


@router.put('/api/users/{user_id}')
@has_role(["Admin"])
async def update_user(user_id: str, user: User, role: str = Depends(verify_token)):
    updated_user = UserController.update_user(user_id, user)
    if updated_user:
        return HTTPResponse(updated_user, 200)
    else:
        return HTTPResponse({"message": "User not found"}, 404)


@router.delete('/api/users/{user_id}')
@has_role(["Admin"])
async def delete_user(user_id: str, role: str = Depends(verify_token)):
    deleted_status = UserController.delete_user(user_id)
    delete_cart_status = CartController.delete_cart(user_id)
    if deleted_status and delete_cart_status:
        return HTTPResponse(status_code=204)
    else:
        return HTTPResponse({"message": "User id not found"}, 404)
