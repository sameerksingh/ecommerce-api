from app.controllers.product_controller import ProductController
from fastapi import APIRouter, Depends
from utils import HTTPResponse, verify_token, has_role
from app.models.product import Product_without_id, Product_update

router = APIRouter(tags=["product"])


@router.get('/api/products/')
@has_role(["Admin", "Customer"])
async def get_products(role: str = Depends(verify_token)):
    print(role)
    products = ProductController.get_all_products()
    return HTTPResponse(content=products)


@router.get('/api/products/{product_id}')
@has_role(["Admin", "Customer"])
async def get_product(product_id, by_name: bool = False, role: str = Depends(verify_token)):
    if by_name:
        product = ProductController.get_product_by_name(product_id)
    else:
        product = ProductController.get_product_by_id(product_id)
    if product:
        return HTTPResponse(content=product)
    else:
        return HTTPResponse({"message": "Product not found"}, 404)


@router.post('/api/products/')
@has_role(["Admin"])
async def add_product(product_data: Product_without_id, role: str = Depends(verify_token)):
    product_id_data = ProductController.add_product(product_data)
    return HTTPResponse(product_id_data, 201)


@router.patch('/api/products/{product_id}')
@has_role(["Admin"])
async def update_product(product_id: str, updated_product_data: Product_update, role: str = Depends(verify_token)):
    try:
        product = ProductController.update_product(product_id, updated_product_data)
        return HTTPResponse(product, 200)
    except ValueError as e:
        return HTTPResponse({"message": e}, 404)


@router.delete('/api/products/{product_id}')
@has_role(["Admin"])
async def delete_product(product_id: str, role: str = Depends(verify_token)):
    deleted_status = ProductController.delete_product(product_id)
    if deleted_status:
        return HTTPResponse(status_code=204)
    else:
        return HTTPResponse({"message": "Product not found"}, 404)