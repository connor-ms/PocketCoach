from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from src import database as db
import sqlalchemy
from sqlalchemy import text

router = APIRouter(
    prefix="/meal-plan",
    tags=["Meal Plan"],
)

class MealPlanCreate(BaseModel):
    user_id: int
    start_date: str
    end_date: str
    daily_calorie_goal: int

class MealLog(BaseModel):
    date: str
    recipe_id: int
    quantity: int
    meal_type: str  

@router.post("/meal-plans")
def create_meal_plan(plan: MealPlanCreate):
    with db.engine.begin() as connection:
        result = connection.execute(
            text("""
                INSERT INTO meal_plans (user_id, start_date, end_date, daily_calorie_goal)
                VALUES (:user_id, :start_date, :end_date, :daily_calorie_goal)
                RETURNING id
            """),
            {
                "user_id": plan.user_id,
                "start_date": plan.start_date,
                "end_date": plan.end_date,
                "daily_calorie_goal": plan.daily_calorie_goal
            }
        )
        meal_plan_id = result.scalar()
    return {"meal_plan_id": meal_plan_id}


@router.post("/meal-plans/{meal_plan_id}/log")
def log_meal(meal_plan_id: int, meal: MealLog):
    with db.engine.begin() as connection:
        connection.execute(
            text("""
                INSERT INTO meal_logs (meal_plan_id, date, recipe_id, quantity, meal_type)
                VALUES (:meal_plan_id, :date, :recipe_id, :quantity, :meal_type)
            """),
            {
                "meal_plan_id": meal_plan_id,
                "date": meal.date,
                "recipe_id": meal.recipe_id,
                "quantity": meal.quantity,
                "meal_type": meal.meal_type
            }
        )
    return {"message": "Meal logged successfully"}

@router.get("/meal-plans/{meal_plan_id}/calories")
def get_daily_calories(meal_plan_id: int, date: str):
    with db.engine.begin() as connection:
        result = connection.execute(text("""
            SELECT COALESCE(
                SUM(
                    ri.quantity * COALESCE(
                        CAST(m.energy_amount AS double precision),
                        u.energy_amount,
                        un.energy_amount
                    )
                ),
                0
            ) AS total_calories
            FROM meal_logs ml
            JOIN recipe_ingredients ri ON ml.recipe_id = ri.recipe_id
            LEFT JOIN menustat m ON ri.ingredient_id = m.menustat_id
            LEFT JOIN usda_branded u ON ri.ingredient_id = u.fdc_id
            LEFT JOIN usda_non_branded un ON ri.ingredient_id = un.id
            WHERE ml.meal_plan_id = :meal_plan_id AND ml.date = :date
        """), {"meal_plan_id": meal_plan_id, "date": date})
        
        total_calories = result.fetchone()[0]
    
    return {"date": date, "total_calories": total_calories}
