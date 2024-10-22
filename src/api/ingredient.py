from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/ingredient",
    tags=["Ingredient"],
)

@router.post("/create")
def ingredient_create():
    
    # with db.engine.begin() as connection:
    #     connection.execute(sqlalchemy.text("""INSERT INTO ingredient VALUES ()"""))

    return "OK"