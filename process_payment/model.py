from typing import Any
from pydantic import BaseModel, field_validator
from datetime import datetime

class PaymentRequest(BaseModel):
    amount: float
    card_number: str
    expiration_date: str
    cvv: str

    @field_validator('amount')
    def validate_amount(cls , v):
        if v == 0.0:
            raise ValueError("Amount can not be zero")
        return v
            
    
    @field_validator('card_number')
    def validate_card_number(cls, v):
        if not v.isdigit():
            raise ValueError("Card number must contain only digits")
        if len(v) != 16:
            raise ValueError("Card number must be exactly 16 digits long")
        return v

    @field_validator('expiration_date')
    def validate_expiration_date(cls, v):
        try:
            expiration_date = datetime.strptime(v, "%m/%Y")
            if expiration_date < datetime.now():
                raise ValueError("Expiration date must be in the future")
        except ValueError:
            raise ValueError("Invalid expiration date format. Use MM/YYYY")
        return v
    
    @field_validator('cvv')
    def validate_cvv(cls, v):
        if not v.isdigit() or len(v) != 3:
            raise ValueError("CVV must be a 3-digit number")
        return v