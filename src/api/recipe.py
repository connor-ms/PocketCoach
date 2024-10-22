from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/recipe",
    tags=["Recipe"],
)

# @router.post("/create")
# def user_create():
    
    # with db.engine.begin() as connection:
        

    # return "OK"