# Path-query-ass2

## Path Parameters

1. Write a FastAPI route that accepts a path parameter for user identification
(user_id) and returns the user's profile information.

2. Implement error handling for the case when the user_id path parameter is
missing.
  #### solution

    ''' python code


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

    '''


## Code Writing: Query Parameters

1. Create a FastAPI route that accepts query parameters for filtering a list of
products by category and price range.

2. Implement default values for the query parameters (category defaulting to 'all'
and price_range defaulting to a specific range).

#### solution
'''


    from fastapi import FastAPI
    from typing import List

    app = FastAPI()

    products = {
    "microwave": {"name": "microwave", "category": "electronics", "price": 500},
    "vintage": {"name": "vintage", "category": "clothings", "price": 300},
    "richDad": {"name": "richDad", "category": "books", "price": 600}
    }



    @app.get('/product')
    async def get_product_query(category: str = 'all', min_price: float = None, max_price: float = None) -> List[dict]:
    """
    Get products based on category and price range.
    
    :param category: Category to filter products by. Defaults to 'all'.
    :param min_price: Minimum price of products to filter by.
    :param max_price: Maximum price of products to filter by.
    :return: List of products matching the criteria.
    """
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


'''




## Combining Path and Query Parameters:
1. Write a FastAPI route that accepts a path parameter for city (city_id) and query
parameters for filtering restaurants by cuisine type (cuisine) and rating
(min_rating).

2. Ensure that the city ID is a path parameter while cuisine type and minimum rating
are query parameters.

#### solution

'''python

    from fastapi import FastAPI , Query
    from typing import Optional , Annotated

    app = FastAPI()


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



'''
## Data Validation:

Modify an existing FastAPI route that accepts a path parameter for user_id to
ensure that user_id is an integer and greater than zero.
Add validation to a query parameter start_date to ensure it is a valid date format

#### solution
'''

    from fastapi import FastAPI, Path, Query, HTTPException
    from datetime import datetime

    app = FastAPI()

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


'''

## Usage and Benefits:



Analyze a given FastAPI application and identify instances where using path
parameters would be more appropriate than query parameters, and vice versa.
Discuss the benefits of using path and query parameters in the provided FastAPI
application and how it enhances API design.


To analyze the given FastAPI application and identify instances where using path parameters would be more appropriate than query parameters, and vice versa, let's consider the following:

### Instances where Path Parameters are More Appropriate:
1. **Unique Resource Identification**:
   - If an endpoint is intended to retrieve, update, or delete a specific resource identified by a unique identifier, such as user ID, product ID, etc., path parameters are more appropriate. For example:
     - `/user/{user_id}`
     - `/product/{product_id}`

2. **Readability and Explicitness**:
   - Path parameters make the endpoint more explicit and readable by directly embedding the identifier in the URL path, making it clear what the endpoint is addressing.

### Instances where Query Parameters are More Appropriate:
1. **Filtering and Pagination**:
   - Query parameters are suitable for filtering resources based on various criteria without modifying the URL structure. For example:
     - `/products?category=electronics`
     - `/users?role=admin&active=true`

2. **Optional Parameters**:
   - Query parameters are useful when certain parameters are optional and don't affect the main resource identification. For instance, filtering by date, sorting order, or pagination parameters.
     - `/items?start_date=2022-01-01&end_date=2022-12-31`
     - `/orders?limit=10&offset=20`

### Benefits of Using Path and Query Parameters in API Design:
1. **Clarity and Readability**:
   - Proper use of path and query parameters enhances the clarity and readability of API endpoints. Path parameters indicate the main resource being accessed, while query parameters provide additional filtering or pagination options.

2. **Predictability**:
   - Path parameters make API endpoints predictable and intuitive, especially for identifying specific resources. Query parameters allow for flexible filtering and customization without altering the core URL structure.

3. **Consistency and Standardization**:
   - Following a consistent pattern for using path and query parameters across API endpoints improves standardization and simplifies client implementation. It ensures that developers understand how to interact with different parts of the API consistently.

4. **Improved Caching and Performance**:
   - Path parameters are typically more suitable for caching purposes as they represent unique resource identifiers. Query parameters, especially for filtering, might lead to varying URLs for the same resource, potentially complicating caching strategies.

5. **Versioning and Flexibility**:
   - Path parameters are often used for versioning APIs, providing a clear indication of the API version being accessed. Query parameters offer flexibility for introducing new parameters or features without breaking existing client implementations.

By carefully selecting between path and query parameters based on the specific requirements of each API endpoint, developers can create APIs that are intuitive, flexible, and easy to use, ultimately enhancing the overall user experience.