from fastapi.testclient import TestClient
from main import app
from model import UserRegistration

client = TestClient(app)

def test_register_user():
    # Define a user registration payload using the UserRegistration model
    user_data = UserRegistration(
        username="testuser",
        email="test@example.com",
        password="Test@1234"  # Meets the password requirements
    )
    
    # Send a POST request to the /register endpoint
    response = client.post("/register", json=user_data.model_dump())
    
    # Assert that the response status code is 422
    assert response.status_code == 422
    
    # Assert that the response contains the expected user data
    expected_response = {"detail": [{"input": None, "loc": ["body", "user"], "msg": "Field required", "type": "missing", "url": "https://errors.pydantic.dev/2.6/v/missing"}]}
    assert response.json() == expected_response

