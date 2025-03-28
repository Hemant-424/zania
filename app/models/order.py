from pydantic import BaseModel, Field
from typing import List, Dict

class OrderItem(BaseModel):
    product_id: int
    quantity: int

# class Order(BaseModel):
#     # order_id: int = Field(..., example=1)  
#     products: List[OrderItem]
#     # total_price: float = Field(..., example=2999.98)  #calculated by system
#     status: str = Field(..., example="pending")

class Order(BaseModel):
    # id: str = Field(..., json_schema_extra={"example": "ORDER-HGJDKLZX"})
    products: List[OrderItem]
    # total_price: float = Field(..., json_schema_extra={"example": 1999.98})   ##calculated by system
    status: str = Field(..., json_schema_extra={"example": "pending"})


class OrderResponse(BaseModel):
    order_id: int
    products: List[OrderItem]
    total_price: float
    status: str