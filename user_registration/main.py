from fastapi import FastAPI,  Body
from model import *

app=FastAPI()

# Route for user registration
@app.post("/register")
async def register_user(user: UserRegistration = Body(..., embed=True)):
    return user.model_dump()