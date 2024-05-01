from app.models.cart import Cart
from app.models.user import UserInDB
from app.controllers.user_controller import UserController
from app.controllers.product_controller import ProductController
from typing import Union
from bson import ObjectId
from utils import mongo_client


class CartController:
    @staticmethod
    def get_cart_by_user_id(user_id: str) -> Union[Cart, None]:
        """
        Retrieve the cart for a user by user ID.
        Args:
            user_id (str): ID of the user.
        Returns:
            Cart: User's cart.
        """
        cart_data = mongo_client.db.carts.find_one({"user_id": user_id})
        if cart_data:
            return Cart(**cart_data)
        else:
            return None

    @staticmethod
    def update_cart(cart: Cart) -> Union[UserInDB, None]:
        """
        Update the cart for a user.
        Args:
            cart (Cart): User's cart.
        Returns:
            UserInDB: Updated user details.
        """
        # Update the cart in the database
        result = mongo_client.db.carts.replace_one(
            {"user_id": cart.user_id}, cart.dict()
        )
        if result.modified_count > 0:
            return CartController.get_cart_by_user_id(cart.user_id)
        else:
            return None

    @staticmethod
    def insert_product_in_cart(user_id: str, product_id: str, quantity: int) -> Cart:
        """
        Insert product in the cart for a user.
        Args:
            user_id (str): User id
            product_id (str): Product id
            quantity (int): Quantity
        Returns:
            UserInDB: Updated user details.
        """

        ObjectId(user_id)
        ObjectId(product_id)
        if not UserController.get_user_by_id(user_id):
            raise Exception("User id does not exist")
        if not ProductController.get_product_by_id(product_id):
            raise Exception("Product id does not exist")

        query = {"user_id": user_id, "products.id": product_id}
        product_in_cart = mongo_client.db.carts.find_one(query)
        if product_in_cart:
            update_operation = {"$inc": {"products.$.quantity": quantity}}
            # Update the cart
            mongo_client.db.carts.update_one(query, update_operation)
            remove_operation = {"$pull": {"products": {"quantity": 0}}}
            # Remove any product with qty = 0
            mongo_client.db.carts.update_one(query, remove_operation)

        else:
            product = ProductController().get_product_by_id(product_id)
            if not product:
                raise Exception("Product_id " + str(product_id) + " does not exist")
            del product
            query = {
                "user_id": user_id,
            }
            update_operation = {
                "$addToSet": {"products": {"id": product_id, "quantity": quantity}}
            }
            # Update the cart
            mongo_client.db.carts.update_one(query, update_operation)

        return CartController.get_cart_by_user_id(user_id)

    @staticmethod
    def create_cart(user_id: str) -> Cart:
        cart = {"user_id": user_id, "products": []}
        mongo_client.db.carts.insert_one(cart)
        return Cart(**cart)

    @staticmethod
    def delete_cart(user_id: str) -> bool:
        ObjectId(user_id)
        result = mongo_client.db.carts.delete_one({"user_id": user_id})
        return result.deleted_count > 0
