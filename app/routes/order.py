from fastapi import FastAPI, APIRouter, HTTPException, Depends
from app.models.order import  Order, OrderItem, OrderResponse
from app.database import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from app.utility import generate_unique_id

order_router = APIRouter()


@order_router.post("/", response_model=OrderResponse)
async def create_order(order: Order, db: AsyncIOMotorDatabase = Depends(get_db)):
    total_price = 0
    product_updates = []
    
    # Check stock availability
    for item in order.products:
        product = await db.products.find_one({"product_id": item.product_id})
        # print(product)
        if not product:
            raise HTTPException(status_code=400, detail=f"Product {item.product_id} not found")
        if product["stock"] < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {item.product_id}")
        
        total_price += product["price"] * item.quantity
        product_updates.append({"product_id": item.product_id, "new_stock": product["stock"] - item.quantity})
    
    # Apply stock updates after all checks
    for update in product_updates:
        await db.products.update_one({"product_id": update["product_id"]}, {"$set": {"stock": update["new_stock"]}})
    
    order_dict = order.model_dump()
    # Generate a unique order ID
    order_dict["order_id"] = generate_unique_id(1000, 9999)
    order_dict["total_price"] = total_price
    order_dict["status"] = "pending"
    result = await db.orders.insert_one(order_dict)

    inserted_order = await db.orders.find_one({"_id": result.inserted_id})
    inserted_order["_id"] = str(inserted_order["_id"])
    if inserted_order:
        return inserted_order

    

@order_router.get("/", response_model=List[OrderResponse])
async def get_orders(db: AsyncIOMotorDatabase = Depends(get_db)):
    return await db.orders.find().to_list(100)

@order_router.get("/{order_id}/", response_model=OrderResponse)
async def get_order(order_id: int, db: AsyncIOMotorDatabase = Depends(get_db)):
    order = await db.orders.find_one({"order_id": order_id})
    print(order)
    if not order:
        raise HTTPException(status_code=404, detail="order not found")
    return order

@order_router.put("/{order_id}/confirm", response_model=Order)
async def confirm_order(order_id: int, db: AsyncIOMotorDatabase = Depends(get_db)):
    order = await db.orders.find_one({"order_id": order_id})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order["status"] != "pending":
        raise HTTPException(status_code=400, detail="Order cannot be completed")
    
    await db.orders.update_one({"order_id": order_id}, {"$set": {"status": "completed"}})
    order["status"] = "completed"
    return order

@order_router.delete("/{order_id}/")
async def delete_order(order_id: int, db: AsyncIOMotorDatabase = Depends(get_db)):
    order = await db.orders.find_one({"order_id": order_id})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    await db.orders.delete_one({"order_id": order_id})
    return {"message": "Order deleted"}
