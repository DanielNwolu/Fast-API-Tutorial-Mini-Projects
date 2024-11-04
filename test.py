from fastapi import FastAPI, HTTPException, Body,Query
from pydantic import BaseModel, EmailStr, constr, ValidationError, validator,Field
from typing import List, Optional
import re
from datetime import datetime

app = FastAPI()

# Define a Pydantic model for the Vehicle
class Vehicle(BaseModel):
    id: int = Field(..., description="Unique identifier for the vehicle")
    make: str = Field(..., description="Make of the vehicle")
    model: str = Field(..., description="Model of the vehicle")
    price: float = Field(..., description="Price of the vehicle")

# Sample data for demonstration
vehicles = [
    Vehicle(id=1, make="Toyota", model="Corolla", price=15000.0),
    Vehicle(id=2, make="Honda", model="Civic", price=18000.0),
    Vehicle(id=3, make="Ford", model="Fusion", price=20000.0),
    Vehicle(id=4, make="Toyota", model="Camry", price=25000.0),
    Vehicle(id=5, make="Chevrolet", model="Cruze", price=17000.0),
    Vehicle(id=6, make="Honda", model="Accord", price=22000.0),
    Vehicle(id=7, make="Ford", model="Mustang", price=35000.0),
    Vehicle(id=8, make="Hyundai", model="Elantra", price=16000.0),
    Vehicle(id=9, make="Nissan", model="Altima", price=23000.0),
    Vehicle(id=10, make="BMW", model="3 Series", price=50000.0),
]

# Route to retrieve vehicle details or list of vehicles based on query parameters
@app.get("/vehicles/")
def get_vehicles(
    vehicle_id: Optional[int] = Query(None, description="ID of the vehicle to retrieve"),
    make: Optional[str] = Query(None, description="Make of the vehicle"),
    model: Optional[str] = Query(None, description="Model of the vehicle"),
    price_range: Optional[str] = Query("0-100", description="Price range of the vehicle"),
):
    if vehicle_id is not None:
        for vehicle in vehicles:
            if vehicle.id == vehicle_id:
                return vehicle
        return {"message": "Vehicle not found"}
    else:
        filtered_vehicles = vehicles

        if make.lower():
            filtered_vehicles = [v for v in filtered_vehicles if v.make == make]
        if model.lower():
            filtered_vehicles = [v for v in filtered_vehicles if v.model == model]
        if price_range:
            min_price, max_price = map(float, price_range.split('-'))
            filtered_vehicles = [v for v in filtered_vehicles if min_price <= v.price <= max_price]

        return filtered_vehicles


