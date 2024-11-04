from fastapi import FastAPI
from model import *


app = FastAPI()

@app.post("/process_payment")
def process_payment(payment_request: PaymentRequest):

    print("Payment Amount:", payment_request.amount)
    print("Card Number:", payment_request.card_number)
    print("Expiration Date:", payment_request.expiration_date)
    print("CVV:", payment_request.cvv)


    return {"message": "Payment processed successfully"}