from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/calories",
    tags=["Calories"],
    dependencies=[Depends(auth.get_api_key)],
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
    return "OK"



