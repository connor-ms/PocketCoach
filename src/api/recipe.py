from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db
from src.api.ingredient import get_ingredient


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

        return result.mappings().one()

    raise HTTPException(status_code = 400, detail = "Failed to create recipe.")


class Ingredient(BaseModel):
    ingredient_id: float
    quantity: float


@router.post("/{recipe_id}/ingredients")
def add_ingredient(recipe_id: int, ingredient: Ingredient):
    with db.engine.begin() as connection:
        ingredients = connection.execute(sqlalchemy.text(
            "SELECT 1 FROM usda_branded WHERE fdc_id = :ingredient_id"),
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

        return Response(status_code=200)

    raise HTTPException(status_code = 400, detail = "Failed to add ingredient.")

@router.delete("/{recipe_id}/ingredients")
def remove_ingredient(recipe_id: int, ingredient_id: int):
    with db.engine.begin() as connection:
        ingredients = connection.execute(sqlalchemy.text(
            "SELECT 1 FROM usda_branded WHERE fdc_id = :ingredient_id"),
            { "ingredient_id": ingredient_id }
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
            "DELETE FROM recipe_ingredients WHERE recipe_id = :recipe_id AND ingredient_id = :ingredient_id"),
            { "recipe_id": recipe_id, "ingredient_id": ingredient_id}
        )

        return Response(status_code=200)

    raise HTTPException(status_code = 400, detail = "Failed to remove ingredient.")


@router.get("/{recipe_id}")
def get_recipe(recipe_id: int):
    recipe_info = {}
    try:
        with db.engine.begin() as connection:
            
            validate_recipe = connection.execute(sqlalchemy.text("""SELECT 1 FROM recipes WHERE id = :id"""), {"id": recipe_id}).one_or_none()
            if validate_recipe is None:
                raise Exception("Recipe not found.")

            result = connection.execute(sqlalchemy.text("""
                SELECT author_id, name, ingredient_id, servings, quantity AS ingredient_quantity FROM recipes
                LEFT JOIN recipe_ingredients ON recipes.id = recipe_ingredients.recipe_id
                WHERE recipes.id = :recipe_id
                """),
                { "recipe_id": recipe_id }
            )

            recipe_info = result.mappings().all()

        ingredients = []
        net_calories = 0
        net_protein = 0
        net_fat = 0

        for row in recipe_info:
            if row["ingredient_id"] is None:
                raise Exception("Recipe contains no ingredients.")
            
            ingredient_info = get_ingredient(row["ingredient_id"])

            print(ingredient_info)

            if ingredient_info:
                net_calories += float(ingredient_info["calories_amount"]) if ingredient_info["calories_amount"] else 0
                # net_protein += float(ingredient_info["protein_amount"]) if ingredient_info["protein_amount"] else 0
                # net_fat += float(ingredient_info["fat_amount"]) if ingredient_info["fat_amount"] else 0
                ingredients.append(ingredient_info)

        return {
            "name": recipe_info[0]["name"],
            "created_by": recipe_info[0]["author_id"],
            "servings": recipe_info[0]["servings"],
            "net_calories": net_calories,
            "ingredients": ingredients
        }
    
    # "net_protein": net_protein,
    # "net_fat": net_fat,
    
    except Exception as e:
        raise HTTPException(status_code = 404, detail = f"Error: {e}")