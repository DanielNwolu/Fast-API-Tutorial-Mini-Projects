from datetime import datetime, timedelta
from main import PaymentRequest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_valid_payment():
    payment_data = {
        "amount": 100.0,
        "card_number": "1234567890123456",
        "expiration_date": (datetime.now() + timedelta(days=30)).strftime("%m/%Y"),
        "cvv": "123"
    }
    response = client.post("/process_payment/", json=payment_data)
    assert response.status_code == 200
    # Adjusted assertion based on the actual structure of the response JSON
    assert "Payment processed successfully" in response.text

def test_zero_amount():
    payment_data = {
        "amount": 0.0,
        "card_number": "1234567890123456",
        "expiration_date": (datetime.now() + timedelta(days=30)).strftime("%m/%Y"),
        "cvv": "123"
    }
    response = client.post("/process_payment/", json=payment_data)
    assert response.status_code == 422  # 422 Unprocessable Entity
    assert "Amount can not be zero" in response.text

def test_invalid_card_number():
    payment_data = {
        "amount": 100.0,
        "card_number": "12345",
        "expiration_date": (datetime.now() + timedelta(days=30)).strftime("%m/%Y"),
        "cvv": "123"
    }
    response = client.post("/process_payment/", json=payment_data)
    assert response.status_code == 422  # 422 Unprocessable Entity
    assert "Card number must be exactly 16 digits long" in response.text

def test_expired_card():
    payment_data = {
        "amount": 100.0,
        "card_number": "1234567890123456",
        "expiration_date": (datetime.now() - timedelta(days=30)).strftime("%m/%Y"),
        "cvv": "123"
    }
    response = client.post("/process_payment/", json=payment_data)
    assert response.status_code == 422  # 422 Unprocessable Entity
    assert "Invalid expiration date format. Use MM/YYYY" in response.text

# Add more test cases as needed

def test_invalid_cvv():
    payment_data = {
        "amount": 100.0,
        "card_number": "1234567890123456",
        "expiration_date": (datetime.now() + timedelta(days=30)).strftime("%m/%Y"),
        "cvv": "12"  # CVV length should be 3 digits
    }
    response = client.post("/process_payment/", json=payment_data)
    assert response.status_code == 422  # 422 Unprocessable Entity
    assert "CVV must be a 3-digit number" in response.text

