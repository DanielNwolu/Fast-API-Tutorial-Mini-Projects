from fastapi import FastAPI
from routes import vehicle_inventory_router

app=FastAPI()
app.include_router(vehicle_inventory_router)



"""
    Vehicle Inventory API:
● Develop a FastAPI endpoint for managing vehicle inventory.
● Use path parameters for vehicle ID and query parameters for filtering by make,
model, and price range.
● Apply numeric validation for vehicle ID and price range.
● Implement string validation for make and model parameters.
● Return details of a specific vehicle identified by ID or a list of vehicles based on
the query parameters.
● Test the API with various combinations of parameters

"""