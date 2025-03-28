from fastapi import FastAPI, APIRouter, HTTPException, Depends
from app.models.product import Product, ProductResponse
from app.database import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from app.utility import generate_unique_id

product_router = APIRouter()



@product_router.get("/", response_model=List[ProductResponse])
async def get_products(db: AsyncIOMotorDatabase = Depends(get_db)):
    all_products = await db.products.find().to_list(100)
    return all_products

@product_router.post("/", response_model=ProductResponse)
async def create_product(product: Product, db: AsyncIOMotorDatabase = Depends(get_db)):
    product_dict = product.model_dump()
    #generate a unique product ID
    product_dict["product_id"] = generate_unique_id(1000, 9999)
    existing_product = await db.products.find_one({"product_id": product_dict["product_id"]})
    if existing_product:
        raise HTTPException(status_code=400, detail="Product ID already exists")
        
    result = await db.products.insert_one(product_dict)

    inserted_product = await db.products.find_one({"_id": result.inserted_id})
    inserted_product["_id"] = str(inserted_product["_id"])
    if inserted_product:
        return inserted_product
    

@product_router.get("/{product_id}/", response_model=ProductResponse)
async def get_product(product_id: int, db: AsyncIOMotorDatabase = Depends(get_db)):
    product = await db.products.find_one({"product_id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@product_router.delete("/{product_id}/")
async def delete_product(product_id: int, db: AsyncIOMotorDatabase = Depends(get_db)):
    existing_product = await db.products.find_one({"product_id": product_id})
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    await db.products.delete_one({"product_id": product_id})
    return {"message": "Product deleted"}