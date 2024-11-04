from fastapi import APIRouter , Path, Query
from typing import Annotated
from services import filter_city_id , filter_query

router = APIRouter()

@router.get("/restuarants")
async def read_restuarants_quary(cuisine: Annotated[str | None , Query(description= " the type of cuisine offered by the restuarants", example="Mexican")] =None , 
min_rating: Annotated[int | None, Query(description= "supply the minimum rate of restuarants" , examples="23")] =None ):
    cuisine= cuisine
    min_rating=min_rating
    
    message = filter_query(cuisine , min_rating)
    return message



@router.get("/restuarants/{city_id}")
async def read_restuarants( city_id : Annotated[int , Path ()]):
    
    city_id =city_id
    
    message =filter_city_id (city_id)
    return message

# @router.get("/restuarants")
# async def read_restuarants_quary(cuisine: Annotated[str | None , Query(description= " the type of cuisine offered by the restuarants", example="Mexican")] =None , 
# min_rating: Annotated[int | None, Query(description= "supply the minimum rate of restuarants" , examples="23")] =None ):
#     cuisine= cuisine
#     min_rating=min_rating
    
#     message = filter_query(cuisine , min_rating)
#     return message