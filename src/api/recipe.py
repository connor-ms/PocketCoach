from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

import sqlalchemy
from src import database as db


router = APIRouter(
    prefix="/recipes",
    tags=["Recipe"],
)


class Recipe(BaseModel):
    author_id: int = None
    name: str = None
    servings: int = None

@router.post("/create")
def create_recipe(recipe: Recipe):
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            "INSERT INTO recipes (author_id, name, servings) VALUES (:id, :name, :servings) RETURNING id"),
            { "id": recipe.author_id, "name": recipe.name, "servings": recipe.servings }
        )

        return result.mappings().one()  

    raise HTTPException(status_code=400, detail="Failed to create user.")


class Ingredient(BaseModel):
    ingredient_id: int
    quantity: int

@router.post("/{recipe_id}")
def create_recipe(recipe_id: int, ingredient: Ingredient):
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text(
            "INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES (:recipe_id, :ingredient_id, :quantity)"),
            { "recipe_id": recipe_id, "ingredient_id": ingredient.ingredient_id, "quantity": ingredient.quantity }
        )

        return { "success": True }

    raise HTTPException(status_code=400, detail="Failed to add ingredient.")