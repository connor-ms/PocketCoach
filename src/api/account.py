from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/accounts",
    tags=["Account"],
    dependencies=[Depends(auth.get_api_key)],
)

class Account(BaseModel):
    user_id: int 
    age: int
    weight: int
    height: int

@router.post("/create")
def create_account(account: Account):
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            "INSERT INTO accounts (user_id, age, weight, height) VALUES (:id, :age, :weight, :height) RETURNING id"),
            { "id": account.user_id, "name": account.age, "servings": account.weight, "height": account.height }
        )

        return result.mappings().one() 

@router.post("/update")
def update_account(account: Account):
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            "UPDATE accounts SET age = :age, weight = :weight, height = :height WHERE user_id = :id"),
            {"id": account.user_id, "age": account.age, "weight": account.weight, "age": account.height}
        )

        return {"success": True}
            
@router.get("/account")
def get_account(account: Account):
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            "SELECT * FROM accounts WHERE user_id = :id"),
            { "id": account.user_id}
        )

        return result.mappings().one() 