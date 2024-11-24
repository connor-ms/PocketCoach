from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from src import database as db
from sqlalchemy import text
router = APIRouter(
    prefix="/meal-plan",
    tags=["Meal Plan"],
)

class MealPlanCreate(BaseModel):
    account_id: int
    name: str
    description: str

class MealLog(BaseModel):
    date: str
    recipe_id: int
    quantity: int
    meal_type: str  

@router.post("/")
def create_meal_plan(plan: MealPlanCreate):
    try:
        with db.engine.begin() as connection:
            validate_account = connection.execute(text(
                    "SELECT id FROM accounts WHERE id = :account_id"),
                    {"account_id": plan.account_id }
                ).one_or_none()

            if validate_account is None:
                raise Exception("Account not found.")

            result = connection.execute(
                text("""
                    INSERT INTO meal_plans (author_id, name, description)
                    VALUES (:account_id, :name, :description)
                    RETURNING id
                """),
                {
                    "account_id": plan.account_id,
                    "name": plan.name,
                    "description": plan.description
                }
            )

            meal_plan_id = result.scalar()
            return {"meal_plan_id": meal_plan_id}
    
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"{e}")

@router.delete("/{meal_plan_id}")
def delete_meal_plan(meal_plan_id: int):
    try:
        with db.engine.begin() as connection:
            validate = connection.execute(
                text("""SELECT 1 FROM meal_plans WHERE id = :meal_plan_id"""),
                {"meal_plan_id": meal_plan_id}
            ).one_or_none()

            if validate is None:
                print(f"Meal Plan with ID {meal_plan_id} not found.")
                raise Exception("Meal Plan not found.")

            connection.execute(
                text("""DELETE FROM plans_recipes WHERE meal_plan_id = :meal_plan_id"""),
                {"meal_plan_id": meal_plan_id}
            )
            connection.execute(
                text("""DELETE FROM meal_plans WHERE id = :meal_plan_id"""),
                {"meal_plan_id": meal_plan_id}
            )

            return Response(status_code=200)
    
    except Exception as e:
        raise HTTPException(
            status_code=404, detail=f"An error occurred while deleting the meal plan: {e}"
        )

@router.post("/{meal_plan_id}/recipes/{recipe_id}")
def add_recipes(meal_plan_id: int,recipe_id: int):
    try: 
        with db.engine.begin() as connection:

            validate_meal_plan = connection.execute(text("""SELECT 1 FROM meal_plans WHERE id = :id"""), {"id": meal_plan_id}).one_or_none()
            if validate_meal_plan is None:
                raise Exception("Meal plan not found.")
            
            validate_recipe = connection.execute(text("""SELECT 1 FROM recipes WHERE id = :id"""), {"id": recipe_id}).one_or_none()

            if validate_recipe is None:
                raise Exception("Recipe not found.")
            
            connection.execute(text("""INSERT INTO plans_recipes (meal_plan_id, recipe_id) VALUES (:meal_plan_id, :recipe_id)"""), {"meal_plan_id": meal_plan_id, "recipe_id": recipe_id})

            return Response(status_code=200)
        
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error adding recipe: {e}")

@router.delete("/{meal_plan_id}/recipes/{recipe_id}")
def remove_recipes(meal_plan_id: int, recipe_id: int):
    try: 
        with db.engine.begin() as connection:

            validate_meal_plan = connection.execute(text("""SELECT 1 FROM meal_plans WHERE id = :id"""), {"id": meal_plan_id}).one_or_none()
            if validate_meal_plan is None:
                raise Exception("Meal plan not found.")
            
            validate_recipe = connection.execute(text("""SELECT 1 FROM recipes WHERE id = :id"""), {"id": recipe_id}).one_or_none()

            if validate_recipe is None:
                raise Exception("Recipe not found.")
            
            validate_meal_recipe = connection.execute(text("""SELECT 1 FROM plans_recipes WHERE meal_plan_id = :meal_plan_id AND recipe_id = :recipe_id"""), 
                                                      {"meal_plan_id": meal_plan_id, "recipe_id": recipe_id}).one_or_none()
            
            if validate_meal_recipe is None:
                raise Exception("Meal plan does not contain recipe.")
            
            connection.execute(text("""DELETE FROM plans_recipes WHERE meal_plan_id = :meal_plan_id AND recipe_id = :recipe_id"""), {"meal_plan_id": meal_plan_id, "recipe_id": recipe_id})

            return Response(status_code=200)
        
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error adding recipe: {e}")

@router.post("/{meal_plan_id}/share")
def share_meal_plan(meal_plan_id: int, author_id: int, recipient_id: int):
    with db.engine.begin() as connection:
        if author_id is recipient_id:
            raise HTTPException(status_code=400, detail="Author id and recipient id can not be the same.")

        try:
            validate_meal_plan = connection.execute(text("""SELECT 1 FROM meal_plans WHERE id = :id AND author_id = :author_id"""), {"id": meal_plan_id, "author_id": author_id}).one_or_none()

            if validate_meal_plan is None:
                    raise Exception("Meal plan and author id combination not found.")
            
            connection.execute(text("""INSERT INTO shared_meal_plans (meal_plan_id, recipient_id) VALUES (:meal_plan_id, :recipient_id)"""), {"meal_plan_id": meal_plan_id, "recipient_id": recipient_id})
            
            return Response(status_code=200)
        
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Error sharing plan: {e}")
        
@router.get("/{account_id}")
def get_meal_plans(account_id: int):
    try:
        with db.engine.begin() as connection:
            validate_user = connection.execute(text("""SELECT 1 FROM accounts WHERE id = :account_id"""), {"account_id": account_id}).one_or_none()

            if validate_user is None:
                raise Exception("Account not found.")

            results = connection.execute(text("""SELECT id, name, description
                                            FROM meal_plans
                                            WHERE author_id = :account_id 
                                            UNION 
                                            SELECT meal_plan_id, name, description FROM shared_meal_plans 
                                            JOIN meal_plans ON shared_meal_plans.meal_plan_id = meal_plans.id 
                                            WHERE recipient_id = :account_id"""), {"account_id": account_id}).mappings().all()
        
            if results:
                return results
            
            return []

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"{e}")

@router.get("/{meal_plan_id}/{account_id}")
def get_meal_plan(meal_plan_id: int, account_id: int):
    try:
        with db.engine.begin() as connection:
            plan = connection.execute(text("""SELECT
                                                    mp.name AS meal_plan_name,
                                                    r.id AS recipe_id,
                                                    r.name AS recipe_name
                                                FROM
                                                meal_plans mp
                                                JOIN plans_recipes pr ON mp.id = pr.meal_plan_id
                                                JOIN recipes r ON pr.recipe_id = r.id
                                                WHERE
                                                    mp.author_id = :account_id AND mp.id = :meal_plan_id"""), 
                                            {"account_id": account_id, "meal_plan_id": meal_plan_id}).mappings().all()
        
            if plan:
                return plan
            
            raise Exception("Meal plan not found that is owned or shared under account id.")

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"{e}")

@router.get("{meal_plan_id}/stats")
def get_plan_stats(meal_plan_id: int):
    try:
        with db.engine.begin() as connection:
            validate_meal_plan = connection.execute(text("""SELECT 1 FROM meal_plans WHERE id = :id"""), {"id": meal_plan_id}).one_or_none()
            if validate_meal_plan is None:
                raise Exception("Meal plan not found.")

            result = connection.execute(text("""
                SELECT
                    r.name AS recipe_name,
                    SUM(i.calories_amount) AS total_calories,
                    SUM(i.protein_amount) AS total_protein,
                    SUM(i.fat_amount) AS total_fat,
                    SUM(i.carb_amount) AS total_carbohydrates
                FROM
                meal_plans mp
                JOIN plans_recipes pr ON mp.id = pr.meal_plan_id
                JOIN recipes r ON pr.recipe_id = r.id
                JOIN recipe_ingredients ri ON r.id = ri.recipe_id
                JOIN usda_branded i ON ri.ingredient_id = i.fdc_id
                WHERE mp.id = :meal_plan_id
                GROUP BY
                    mp.id,
                    r.name;
            """), {"meal_plan_id": meal_plan_id}).mappings().all()
            
            return result

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"{e}")