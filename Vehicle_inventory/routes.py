from fastapi import APIRouter ,Query
from fastapi.responses import JSONResponse
from models import filter_vehicles

vehicle_inventory_router =APIRouter(prefix="/vehicle")

@vehicle_inventory_router.get("/{vehicle_id}")
async def read_inventory (vehicle_id: int ,
make: str =Query(default=None, description="the makers of the vehicle" ),
model: str =Query(default=None, description="model of the vehicle" ),
price_range=Query(default = None, description = "Price range" ) ):
    
    """
    This route can be use to search for vehicle by vehicle_id , make , model and price_range,
    however if the client gives a vehicle_id not in the database , it return all the vehicle in the data base.

    """ 
    vehicle_id =vehicle_id
    make=make
    model =model
    price_range = price_range
   
    message = filter_vehicles(vehicle_id, make , model , price_range)
    return message




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