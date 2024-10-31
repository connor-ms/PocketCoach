from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db


router = APIRouter(
    prefix="/recipes",
    tags=["Recipe"],
    dependencies=[Depends(auth.get_api_key)],
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

    raise HTTPException(status_code = 400, detail = "Failed to create user.")


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

    raise HTTPException(status_code = 400, detail = "Failed to add ingredient.")


@router.get("/{recipe_id}")
def get_recipe(recipe_id: int):
    recipe_info = {}

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
            SELECT * FROM recipes
            JOIN recipe_ingredients ON recipes.id = recipe_ingredients.recipe_id
            WHERE recipe_id = :recipe_id
            """),
            { "recipe_id": recipe_id }
        )

        recipe_info = result.mappings().all()

    ingredients = []

    for row in recipe_info:
        # TODO: use inventory.get_ingredient() once implemented
        ingredients.append({
            "ingredient_id": row["ingredient_id"],
            "quantity": row["quantity"]
        })

    return {
        "name": recipe_info[0]["name"],
        "created_by": recipe_info[0]["author_id"],
        "servings": recipe_info[0]["servings"],
        "ingredients": ingredients,
        # TODO: net_calories, net_protein, net_carbs
    }