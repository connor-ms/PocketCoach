from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel
import sqlalchemy
from src import database as db
from src.api.ingredient import get_ingredient
from datetime import datetime


router = APIRouter(
    prefix="/recipes",
    tags=["Recipe"],
)


class Recipe(BaseModel):
    author_id: float = None
    name: str = None
    servings: float = None


@router.post("/")
def create_recipe(recipe: Recipe):
    start=datetime.now()
    with db.engine.begin() as connection:
        if recipe.servings < 1 or recipe.servings > 100:
            raise HTTPException(status_code=400, detail = "Invalid serving size. Must be between 1 and 100 (inclusive).")

        if recipe.name == "":
            raise HTTPException(status_code=400, detail = "Recipe name can't be blank.")
        
        account = connection.execute(sqlalchemy.text(
            "SELECT id FROM accounts WHERE id = :account_id"),
            { "account_id": recipe.author_id }
        ).mappings().one_or_none()
        
        if account is None:
            raise HTTPException(status_code=400, detail = "Invalid account id.")

        #connection.execution_options(isolation_level="REPEATABLE READ")
        result = connection.execute(sqlalchemy.text(
            "INSERT INTO recipes (author_id, name, servings) VALUES (:id, :name, :servings) RETURNING id"),
            { "id": recipe.author_id, "name": recipe.name, "servings": recipe.servings }
        )
        print(f"execution time: {datetime.now() - start}")
        return result.mappings().one()

    raise HTTPException(status_code = 400, detail = "Failed to create recipe.")


class Ingredient(BaseModel):
    ingredient_id: float
    quantity: float


@router.post("/{recipe_id}/ingredients")
def add_ingredient(recipe_id: int, ingredient: Ingredient):
    start=datetime.now()
    with db.engine.begin() as connection:
        ingredients = connection.execute(sqlalchemy.text(
            "SELECT 1 FROM usda_branded WHERE id = :ingredient_id"),
            { "ingredient_id": ingredient.ingredient_id }
        ).mappings().one_or_none()

        if not ingredients:
            raise HTTPException(status_code=400, detail="Invalid ingredient id given.")
        
        recipe = connection.execute(sqlalchemy.text(
            "SELECT 1 FROM recipes WHERE id = :recipe_id"),
            { "recipe_id": recipe_id }
        ).mappings().one_or_none()

        if not recipe:
            raise HTTPException(status_code=400, detail="Invalid recipe id given.")

        connection.execute(sqlalchemy.text(
            "INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES (:recipe_id, :ingredient_id, :quantity)"),
            { "recipe_id": recipe_id, "ingredient_id": ingredient.ingredient_id, "quantity": ingredient.quantity }
        )
        print(f"execution time: {datetime.now() - start}")
        return Response(status_code=200)

    raise HTTPException(status_code = 400, detail = "Failed to add ingredient.")


@router.get("/{recipe_id}")
def get_recipe(recipe_id: int):
    start=datetime.now()
    recipe_info = {}

    with db.engine.begin() as connection:
        #connection.execution_options(isolation_level= "REPEATABLE READ")
        result = connection.execute(sqlalchemy.text("""
            SELECT * FROM recipes
            JOIN recipe_ingredients ON recipes.id = recipe_ingredients.recipe_id
            WHERE recipe_id = :recipe_id
            """),
            { "recipe_id": recipe_id }
        )

        recipe_info = result.mappings().all()

    if len(recipe_info) == 0:
        raise HTTPException(status_code=400, detail="Invalid recipe id given.")

    ingredients = []
    net_calories = 0
    net_protein = 0
    net_fat = 0

    for row in recipe_info:
        ingredient_info = get_ingredient(row["ingredient_id"])

        if ingredient_info:
            net_calories += float(ingredient_info["calorie_amount"]) if ingredient_info["calorie_amount"] else 0
            net_protein += float(ingredient_info["protein_amount"]) if ingredient_info["protein_amount"] else 0
            net_fat += float(ingredient_info["fat_amount"]) if ingredient_info["fat_amount"] else 0
            ingredients.append(ingredient_info)

    print(f"execution time: {datetime.now() - start}")
    return {
        "name": recipe_info[0]["name"],
        "created_by": recipe_info[0]["author_id"],
        "servings": recipe_info[0]["servings"],
        "net_calories": net_calories,
        "net_protein": net_protein,
        "net_fat": net_fat,
        "ingredients": ingredients
    }