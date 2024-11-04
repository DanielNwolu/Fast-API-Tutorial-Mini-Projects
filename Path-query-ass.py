from fastapi import FastAPI , HTTPException


# Path-query-ass2

## Path Parameters

"""1. Write a FastAPI route that accepts a path parameter for user identification
(user_id) and returns the user's profile information.

2. Implement error handling for the case when the user_id path parameter is
missing."""

from fastapi import FastAPI , HTTPException

app = FastAPI()

users = {
    1: {
        "name": "John Doe",
        "email": "john@example.com"
        },
    2: {
        "name": "Jane Smith",
        "email": "jane@example.com"
        },
    3: {
        "name": "Nwolu David",
        "email" : "nwoludave@gmail.com"
        },
    4: {
        "name": "Nwolu Daniel",
        "email" : "nwoludaniel@gmail.com"
        },

}


@app.get("/users/{user_id}")
async def read_user(user_id: int):

#### Check if the user_id exists in the dictionary
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    #### Retrieve user information
    user_info = users[user_id]

    return user_info




## Code Writing: Query Parameters

"""1. Create a FastAPI route that accepts query parameters for filtering a list of
products by category and price range.

2. Implement default values for the query parameters (category defaulting to 'all'
and price_range defaulting to a specific range)."""

#### solution

products = {
"microwave": {"name": "microwave", "category": "electronics", "price": 500},
"vintage": {"name": "vintage", "category": "clothings", "price": 300},
"richDad": {"name": "richDad", "category": "books", "price": 600}
}



@app.get('/product')
async def get_product_query(category: str = 'all', min_price: float = None, max_price: float = None) -> List[dict]:
    
    filtered_products = []

    if category == 'all':
        return list(products.values())

    for product_name, product_details in products.items():
        # Filtering by category and price range
        if (product_details["category"] == category) and \
           (min_price is None or product_details["price"] >= min_price) and \
           (max_price is None or product_details["price"] <= max_price):
            filtered_products.append({"product": product_name, **product_details})
    
    return filtered_products




## Combining Path and Query Parameters:
"""1. Write a FastAPI route that accepts a path parameter for city (city_id) and query
parameters for filtering restaurants by cuisine type (cuisine) and rating
(min_rating).

2. Ensure that the city ID is a path parameter while cuisine type and minimum rating
are query parameters."""

#### solution

restaurants_db = {
    1: {"name": "Bite Bistro", "cuisine": "African", "rating": 4.5},
    2: {"name": "FlavorSpot", "cuisine": "Italian", "rating": 5},
    3: {"name": "Tasty Twist", "cuisine": "American", "rating": 3.5},
    4: {"name": "Sizzling Grill", "cuisine": "Steakhouse", "rating": 4.2},
    5: {"name": "Spice Avenue", "cuisine": "Indian", "rating": 4.0},
    6: {"name": "Mama Mia", "cuisine": "Italian", "rating": 4.7},
    7: {"name": "Sushi Delight", "cuisine": "Japanese", "rating": 4.3},
    8: {"name": "Grill Master", "cuisine": "Barbecue", "rating": 4.8},
    9: {"name": "Taco Haven", "cuisine": "Mexican", "rating": 4.1},
    10: {"name": "Pho Corner", "cuisine": "Vietnamese", "rating": 4.6}
}



@app.get("/cities/{city_id}")
async def get_city_restaurant(city_id :int , cuisine: str = None ,  min_rating :float = None):  
    if city_id not in restaurants_db:
        return {"message": "City not found"}
# Add return statement to exit the function if city not found
    filtered_restaurants = []
    for key, v in restaurants_db.items():
        if cuisine and cuisine.lower() != v["cuisine"].lower():
            continue  # Skip if cuisine doesn't match
        if min_rating and v["rating"] < min_rating:
            continue  # Skip if rating is lower than required
        filtered_restaurants.append(v)  # Append restaurant name to the list
    return filtered_restaurants

## Data Validation:

"""Modify an existing FastAPI route that accepts a path parameter for user_id to
ensure that user_id is an integer and greater than zero.
Add validation to a query parameter start_date to ensure it is a valid date format"""

#### solution

@app.get("/user/{user_id}")
async def get_user(user_id: int = Path(..., title="The ID of the user", gt=0)):
    """
    Retrieve user information by user_id.
    """
    return {"user_id": user_id}

@app.get("/items/")
async def get_items(start_date: datetime = Query(None, title="Start date", description="The starting date for filtering items", regex=r"\d{4}-\d{2}-\d{2}")):
    """
    Retrieve items with optional filtering by start_date.
    """
    if start_date is not None:
        # If start_date is provided, validate it's a valid date format
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid start_date format. Use YYYY-MM-DD.")
    
    return {"start_date": start_date}


