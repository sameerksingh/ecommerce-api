from app.models.product import Product, ProductWithoutId, ProductUpdate
from utils import document_to_model
from bson import ObjectId
from typing import Union, Any, Mapping
from config import Config
from pymongo import MongoClient

mongo_client: MongoClient[Mapping[str, Any] | Any] = MongoClient(Config.MONGO_URI)


class ProductController:
    @staticmethod
    def get_all_products() -> list[Product]:
        products = list(mongo_client.db.products.find())
        return [document_to_model(Product,product) for product in products]

    @staticmethod
    def get_product_by_id(product_id: str) -> Union[Product, None]:
        product = mongo_client.db.products.find_one({"_id": ObjectId(product_id)})
        if product:
            return document_to_model(Product,product)
        else:
            return None

    @staticmethod
    def get_product_by_name(product_name: str) -> Union[Product, None]:
        product = mongo_client.db.products.find_one({"name": product_name})
        if product:
            return document_to_model(Product,product)
        else:
            return None

    @staticmethod
    def add_product(product: ProductWithoutId) -> Product:
        inserted_product = mongo_client.db.products.insert_one(product.dict())
        product_dict = product.dict()
        product_dict["id"] = str(inserted_product.inserted_id)
        return Product(**product_dict)

    @staticmethod
    def update_product(product_id: str, updated_product_data: ProductUpdate) -> Union[Product, None]:
        try:
            ObjectId(product_id)
        except Exception as e:
            raise ValueError("Invalid product_id")

        product = mongo_client.db.products.find_one({"_id": ObjectId(product_id)})

        if not product:
            raise ValueError("Product not found")
        new_product_data= {key: value for key, value in updated_product_data.dict().items() if value}
        product.update(new_product_data)

        updated_product = mongo_client.db.products.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": product}
        )

        if updated_product.matched_count > 0:
            return ProductController.get_product_by_id(product_id)

    @staticmethod
    def delete_product(product_id: str) -> bool:
        result = mongo_client.db.products.delete_one({"_id": ObjectId(product_id)})
        return result.deleted_count > 0
