from fastapi import FastAPI, HTTPException, Body,Query
from pydantic import BaseModel, EmailStr, constr, ValidationError,validator
import re
from typing import List, Optional
from datetime import datetime

# Initialize FastAPI app
app = FastAPI()

#Question 1
# Pydantic model for request body
class UserRegistration(BaseModel):
    username: constr(min_length=4, max_length=20)
    email: EmailStr

    password: constr(
        min_length=8,
    )

    @validator('password')
    def validate_password(cls, v):
        if not re.match("^(?=.*[A-Z])(?=.*[!@#$%^&*()])(?=.*[0-9]).*$", v):
            raise ValueError(
                "Password must contain at least one uppercase letter, one special character, and one digit"
            )
        return v

# Route for user registration
@app.post("/register")
async def register_user(user: UserRegistration = Body(..., embed=True)):
    return user.model_dump()




# # question 2 assignment 1.
# # Sample product data
products = [
    {"name": "Product A", "category": "Category 1", "price": 10.99},
    {"name": "Product B", "category": "Category 2", "price": 20.49},
    {"name": "Product C", "category": "Category 1", "price": 15.99},
    {"name": "Product D", "category": "Category 3", "price": 30.99},
    {"name": "Product E", "category": "Category 2", "price": 25.49}
]

# # Define query parameters with validation
# @app.get("/products/")
# async def search_products(
#     name: Optional[str] = Query(None, min_length=1, regex="^[a-zA-Z0-9 ]+$"),
#     category: Optional[str] = Query(None, min_length=1, regex="^[a-zA-Z0-9 ]+$"),
#     min_price: Optional[float] = Query(None, ge=0),
#     max_price: Optional[float] = Query(None, ge=0)
# ) -> List[dict]:
#     """
#     Search products based on provided criteria.

#     :param name: Product name to search for.
#     :param category: Product category to filter by.
#     :param min_price: Minimum price of the product.
#     :param max_price: Maximum price of the product.
#     :return: List of products matching the search criteria.
#     """
#     # Filter products based on query parameters
#     filtered_products = products
    
#     if name:
#         filtered_products = [p for p in filtered_products if name.lower() in p['name'].lower()]
    
#     if category:
#         filtered_products = [p for p in filtered_products if category.lower() in p['category'].lower()]
    
#     if min_price is not None:
#         filtered_products = [p for p in filtered_products if p['price'] >= min_price]
    
#     if max_price is not None:
#         filtered_products = [p for p in filtered_products if p['price'] <= max_price]

#     return filtered_products



# Question 3
class PaymentRequest(BaseModel):
    amount: float
    card_number: str
    expiration_date: str
    cvv: str


    @validator('card_number')
    def validate_card_number(cls, v):
        if not v.isdigit():
            raise ValueError("Card number must contain only digits")
        if len(v) != 16:
            raise ValueError("Card number must be exactly 16 digits long")
        return v

    @validator('expiration_date')
    def validate_expiration_date(cls, v):
        try:
            expiration_date = datetime.strptime(v, "%m/%Y")
            if expiration_date < datetime.now():
                raise ValueError("Expiration date must be in the future")
        except ValueError:
            raise ValueError("Invalid expiration date format. Use MM/YYYY")
        return v

    @validator('cvv')
    def validate_cvv(cls, v):
        if not v.isdigit() or len(v) != 3:
            raise ValueError("CVV must be a 3-digit number")
        return v

@app.post("/process_payment")
def process_payment(payment_request: PaymentRequest):

    print("Payment Amount:", payment_request.amount)
    print("Card Number:", payment_request.card_number)
    print("Expiration Date:", payment_request.expiration_date)
    print("CVV:", payment_request.cvv)


    return {"message": "Payment processed successfully"}

# Test with valid and invalid payment data
if __name__ == "__main__":
    from fastapi.testclient import TestClient

    client = TestClient(app)

    # Valid payment data
    valid_payment_data = {
        "amount": 100.0,
        "card_number": "1234567890123456",
        "expiration_date": "12/2024",
        "cvv": "123"
    }

    response = client.post("/process_payment", json=valid_payment_data)
    print("Valid Payment Response:", response.json())

    # Invalid payment data (for testing purposes)
    invalid_payment_data = {
        "amount": "invalid_amount",  # Invalid amount
        "card_number": "1234",  # Invalid card number
        "expiration_date": "13/2024",  # Invalid expiration date
        "cvv": "12"  # Invalid CVV
    }

    response = client.post("/process_payment", json=invalid_payment_data)
    print("Invalid Payment Response:", response.json())



