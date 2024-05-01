from app.models.product import ProductUpdate
from app.models.order import Order
from typing import Union, List
from utils import document_to_model, mongo_client
from bson import ObjectId
from app.controllers.cart_controller import CartController
from app.controllers.product_controller import ProductController
from datetime import datetime


class OrderController:
    @staticmethod
    def get_orders() -> Union[List[Order], None]:
        """
        Retrieves all orders
        Returns:
            Orders: All Order details.
        """
        try:
            orders = mongo_client.db.orders.find({}).sort({"timestamp": -1})
            if orders:
                return [document_to_model(Order, order) for order in orders]
            return None
        except Exception as e:
            return None

    @staticmethod
    def get_order_by_user_id(user_id: str) -> Union[List[Order], None]:
        """
        Retrieve a user by their email address.
        Args:
            user_id (id): User_id of the user.
        Returns:
            Order: User's order details.
        """
        try:
            orders = mongo_client.db.orders.find({"user_id": user_id}).sort(
                {"timestamp": -1}
            )
            if orders:
                return [document_to_model(Order, order) for order in orders]
            return None
        except Exception as e:
            return None

    @staticmethod
    def place_order(user_id: str) -> Order:
        """
        Buy the products inside a cart, update the inventory and place order
        Args:
            user_id (str): User's id.
        Returns:
            Order: Order details.
        """

        # TODO: Add payment gateway

        ObjectId(user_id)
        cart = CartController.get_cart_by_user_id(user_id)
        if not cart:
            raise Exception("User id does not exist")
        order_products = []
        bill = 0
        for product in cart.products:
            product_check = ProductController.get_product_by_id(product.id)
            if not product_check:
                raise Exception("Product_id " + str(product.id) + " does not exist")
            if product.quantity > product_check.inventory:
                product.quantity = product_check.inventory
            bill += product.quantity * product_check.price
            updated_product_data = {
                "inventory": product_check.inventory - product.quantity
            }
            ProductController.update_product(
                product.id, ProductUpdate(**updated_product_data)
            )
            product_dict = product_check.dict()
            product_dict["quantity"] = product.quantity
            del product_dict["inventory"]
            order_products.append(product_dict)
        order_dict = cart.dict()
        order_dict["products"] = order_products
        order_dict["bill"] = round(bill, 2)
        order_dict["timestamp"] = datetime.now()
        order = Order(**order_dict)
        mongo_client.db.orders.insert_one(order.dict())
        return order
