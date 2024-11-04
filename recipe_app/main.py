from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
import json

# Initialize FastAPI app
app = FastAPI()

# Define Pydantic models
class NutritionalInfo(BaseModel):
    calories: float
    fat: float
    protein: float

class Ingredient(BaseModel):
    name: str
    quantity: float

class Recipe(BaseModel):
    id: int
    title: str
    description: str
    instructions: str
    ingredients: List[Ingredient]
    nutritional_info: NutritionalInfo = None

# Function to read recipes from JSON file
def read_recipes_from_file() -> List[Recipe]:
    with open("recipes.json", "r") as file:
        recipes = json.load(file)
        return recipes

# Function to write recipes to JSON file
def write_recipes_to_file(recipes: List[Recipe]):
    with open("recipes.json", "w") as file:
        json.dump(recipes, file, indent=4)

# Function to append a new recipe to JSON file
def append_recipe_to_file(recipe: Recipe):
    recipes = read_recipes_from_file()
    recipe_dict = recipe.dict()
    recipe_dict.pop("id")  # Remove id before appending
    recipes.append(recipe_dict)
    write_recipes_to_file(recipes)

# Function to get recipe by ID
def get_recipe_by_id(recipe_id: int) -> Optional[Recipe]:
    recipes = read_recipes_from_file()
    for recipe in recipes:
        if recipe["id"] == recipe_id:
            return Recipe(**recipe)
    return None

# Function to delete recipe by ID
def delete_recipe_by_id(recipe_id: int):
    recipes = read_recipes_from_file()
    for i, recipe in enumerate(recipes):
        if recipe["id"] == recipe_id:
            del recipes[i]
            write_recipes_to_file(recipes)
            return
    raise HTTPException(status_code=404, detail="Recipe not found")

# CRUD operations for recipes
@app.get("/recipes/", response_model=List[Recipe])
def get_recipes(title: Optional[str] = None,
                ingredient: Optional[str] = None,
                calories_less_than: Optional[float] = None):
    recipes = read_recipes_from_file()

    # Filtering logic goes here

    return recipes

@app.post("/recipes/", response_model=Recipe)
def create_recipe(recipe: Recipe):
    recipes = read_recipes_from_file()
    new_recipe_id = len(recipes) + 1
    recipe.id = new_recipe_id
    append_recipe_to_file(recipe)
    return recipe

@app.get("/recipes/{recipe_id}", response_model=Recipe)
def get_recipe(recipe_id: int):
    recipe = get_recipe_by_id(recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@app.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int):
    delete_recipe_by_id(recipe_id)
    return {"message": "Recipe deleted successfully"}
