from fastapi import HTTPException
import json


restuarants=[]
file = "restuarant.json"

with open (file,"r") as f:
    data = f.read()
    restuarants= json.loads(data)
    

def filter_city_id (city_id):
    try:
        for restuarant in restuarants:
            if city_id and restuarant.get("city_id") == city_id:
                return {"restuarant": restuarant}
            else:   
                raise HTTPException(status_code=404, detail="no restuarant found for the provided parameter")
    except HTTPException as e:
        return {"error": e}
    
def  filter_query( cuisine , min_rating):
    try:
        filtered_restuarants = []

        for restuarant in restuarants:
            if cuisine and cuisine.lower() not in restuarant["cuisine"].lower():
                continue
            if min_rating and restuarant["min_rating"] != min_rating:
                continue
            filtered_restuarants.append(restuarant)
        if filtered_restuarants:
            return {"restuarant": filtered_restuarants}
        else:  
            raise HTTPException(status_code=404, detail="no product found for the provided parameter")

    except HTTPException as e:
        return {"error": e}