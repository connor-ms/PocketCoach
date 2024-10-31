from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/meal-plan",
    tags=["Meal Plan"],
    dependencies=[Depends(auth.get_api_key)],
)

# @router.post("/create")
# def user_create():
    
    # with db.engine.begin() as connection:
        

    # return "OK"