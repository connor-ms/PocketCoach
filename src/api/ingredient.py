from fastapi import APIRouter, Depends, HTTPException, Request, Response
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
    description: str
    serving_size_unit: str
    serving_size: int
    calories: int

def validate_range(value: int, min: int, max: int, attribute: str):
    if value < min:
        raise Exception(f"{attribute} is invalid, must be {min} or above.")
    elif value >= max:
        raise Exception(f"{attribute} is invalid, must be {max} or below.")

def validate_info(ingredient: Ingredient) -> bool:
    validate_range(ingredient.calories, 0, 2000, "Calories")
    validate_range(ingredient.serving_size, 1, 50, "Serving size")

@router.post("/")
def create_ingredient(ingredient: Ingredient):
    try:
        validate_info(ingredient)

        ingredient_data = ingredient.dict()

        with db.engine.begin() as connection:
            stmt = sqlalchemy.insert(db.ingredients).values(ingredient_data)
            result = connection.execute(stmt.returning(db.ingredients.c.fdc_id))
            return result.mappings().one()

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {e}")
    
@router.put("/{ingredient_id}")
def update_ingredient(ingredient_id, ingredient: Ingredient):
    try:
        validate_info(ingredient)

        ingredient_data = ingredient.dict()

        with db.engine.begin() as connection:
            stmt = sqlalchemy.update(db.ingredients).values(ingredient_data).where(db.ingredients.c.fdc_id == ingredient_id)
            connection.execute(stmt)
            
            return Response(status_code=200)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {e}")
    
@router.delete("{ingredient_id}")
def delete_ingredient(ingredient_id):
    try:
        with db.engine.begin() as connection:
            result = connection.execute(sqlalchemy.text("""DELETE FROM usda_branded WHERE fdc_id = :id"""), {"id": ingredient_id})
            return Response(status_code=200)
        
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid ingredient id. Please try and enter another id.")
    
@router.get("/id/{ingredient_id}")
def get_ingredient(ingredient_id: int):
    try:
        with db.engine.begin() as connection:
            print(ingredient_id)
            result = connection.execute(sqlalchemy.text("SELECT * FROM usda_branded WHERE fdc_id = :id"), {"id": ingredient_id})
            value = result.mappings().one_or_none()
        
            if value is None:
                raise Exception(f"Incorrect ingredient id ({ingredient_id})")

            return value
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {e}")
    
@router.get("/name/{ingredient_name}")
def get_ingredients_by_name(ingredient_name: str, page: int):
    try:
        if page >= 0:
            offset = page * 10
        else:
            raise Exception("Page number needs to be greater than or equal to 0.")
        
        with db.engine.begin() as connection:
            result = connection.execute(sqlalchemy.text("""SELECT * FROM usda_branded WHERE description ILIKE :name LIMIT 10 OFFSET :offset"""), {"name": ingredient_name, "offset": offset})

            return result.mappings().all()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid Inputs: {e}")