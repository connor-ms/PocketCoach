from fastapi import APIRouter
from pydantic import BaseModel
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/calories",
    tags=["Calories"],
)

# @router.post("/create")
# def user_create():
    
    # with db.engine.begin() as connection:
        

    # return "OK"