from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"],
)

class Account(BaseModel):
    first_name: str
    last_name: str
    age: int
    weight: int
    height: int

@router.post("/create")
def create_account(account: Account):
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            "INSERT INTO accounts (first_name, last_name, age, weight, height) VALUES (:first_name, :last_name, :age, :weight, :height) RETURNING id"),
            {"first_name": account.first_name, "last_name": account.last_name, "age": account.age, "weight": account.weight, "height": account.height }
        )

        return result.mappings().one() 
    
    raise HTTPException(status_code = 400, detail = "Failed to create user.")

@router.post("/update/{id}")
def update_account(id: int, account: Account):
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            "UPDATE accounts SET age = :age, weight = :weight, height = :height WHERE id = :id"),
            {"id": id, "first_name": account.first_name, "last_name": account.last_name, "age": account.age, "weight": account.weight, "height": account.height}
        )

        return {"success": True}
    
    raise HTTPException(status_code = 400, detail = "Failed to update user.")
            
@router.get("/{id}")
def get_account(id: int):
    
    
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            "SELECT id, first_name, last_name, age, weight, height FROM accounts WHERE id = :id"),
            { "id": id}
        )

        res = result.mappings().first()

        if res:
            return{
                "first_name": res.first_name,
                "last_name": res.last_name,
                "age": res.age,
                "weight": res.weight,
                "height": res.height
            }

    raise HTTPException(status_code = 400, detail = "Invalid Account.")
     


    
        
    

    