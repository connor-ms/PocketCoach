from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db


router = APIRouter(
    prefix="/ingredient",
    tags=["Ingredient"],
    dependencies=[Depends(auth.get_api_key)],
)

class Ingredient(BaseModel):
    name: str
    serving_size_type: str
    serving_size: int
    calories: int

@router.post("/")
def ingredient_create(ingredient: Ingredient):
    
    # with db.engine.begin() as connection:
    #     connection.execute(sqlalchemy.text("""INSERT INTO ingredient VALUES ()"""))

    #TODO: Once DB is setup change this to return ID
    return ingredient

@router.put("/{ingredient_id}")
def ingredient_update(ingredient: Ingredient):

    return ingredient

@router.delete("{ingredient_id}")
def ingredient_delete(ingredient: Ingredient):

    return "OK"

@router.get("/{ingredient_id}")
def get_ingredient(ingredient_id: int):
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text("SELECT * FROM usda_branded WHERE fdc_id = :id"), {"id": ingredient_id})
        return result.mappings().first()

@router.get("/")
def get_ingredients():
    ingredients = [{}]

    return ingredients