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
def add_ingredient(recipe_id: int, ingredient: Ingredient):
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text(
            "INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES (:recipe_id, :ingredient_id, :quantity)"),
            { "recipe_id": recipe_id, "ingredient_id": ingredient.ingredient_id, "quantity": ingredient.quantity }
        )

        return { "success": True }

    raise HTTPException(status_code=400, detail="Failed to add ingredient.")


@router.get("/{recipe_id}")
def create_recipe(recipe_id: int):
    recipe_info = {}

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
            SELECT * FROM recipes
            JOIN recipe_ingredients ON recipes.id = recipe_ingredients.recipe_id
            LEFT JOIN usda_branded ON usda_branded.fdc_id = recipe_ingredients.ingredient_id
            LEFT JOIN usda_non_branded ON usda_non_branded.fdc_id = recipe_ingredients.ingredient_id
            LEFT JOIN menustat ON menustat.menustat_id = recipe_ingredients.ingredient_id
            WHERE recipe_id = :recipe_id
            """),
            { "recipe_id": recipe_id }
        )

        recipe_info = result.mappings().one()

    return recipe_info