from fastapi import Query
from pydantic import BaseModel, EmailStr
from typing import  Annotated


class Product(BaseModel):
    name:str
    category: str
    price_range: int |None = None
    email: EmailStr
    
@app.post("/product")
async def create_product (product:Product , q: Annotated [str | None , Query(min_length =30)]):
    print (f"The product name is {product.name}")
    return product
    