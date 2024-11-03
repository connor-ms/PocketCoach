from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/calories",
    tags=["Calories"],
)

class Calories(BaseModel):
    calories_consumed: int = None
    calories_burned: int = None

@router.post("/create")
def add_calories_consumed(calories: Calories):
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text(
            "INSERT INTO calories (calories_consumed) VALUES (:calories_consumed) RETURNING id"),
            { "calories_consumed": calories.calories_consumed }
        )

        return {"success": True}
    raise HTTPException(status_code = 400, detail = "Failed to add calories consumed.")

#need to add logic for calories burned against calories added.
@router.post("/create")
def add_calories_burned(calories: Calories):
    with db.engine.begin() as connection:
        connection.execeute(sqlalchemy.text(
            "INSERT INTO calories (calories_burned) VALUES "),
            { "calories_consumed": calories.calories_burned }
        )

        return {"success": True}
    
    raise HTTPException(status_code = 400, detail = "Failed to add calories burned.")

