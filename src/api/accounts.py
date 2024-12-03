from fastapi import APIRouter, HTTPException, Depends, Response
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

def validate_range(value: int, min: int, max: int, attribute: str):
    if value < min:
        raise HTTPException(status_code=400, detail=f"{attribute} is invalid, must be above {min}.")
    elif value > max:
        raise HTTPException(status_code=400, detail=f"{attribute} is invalid, must be below {max}.")

def validate_info(account: Account) -> bool:
    validate_range(account.age, 12, 100, "Age")
    validate_range(account.weight, 80, 450, "Weight")
    validate_range(account.height, 50, 100, "Height")

@router.post("/create")
def create_account(account: Account):
    validate_info(account)
    
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            "INSERT INTO accounts (first_name, last_name, age, weight, height) VALUES (:first_name, :last_name, :age, :weight, :height) RETURNING id"),
            {"first_name": account.first_name, "last_name": account.last_name, "age": account.age, "weight": account.weight, "height": account.height })

        return result.mappings().one() 
    
    raise HTTPException(status_code = 400, detail = "Failed to create user.")
    
@router.put("/update/{account_id}")
def update_account(id: int, account: Account):
    validate_info(account)

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            "UPDATE accounts SET first_name = :first_name, last_name = :last_name, age = :age, weight = :weight, height = :height WHERE id = :id"),
            {"id": id, "first_name": account.first_name, "last_name": account.last_name, "age": account.age, "weight": account.weight, "height": account.height}
        )

        return Response(status_code=200)
    
    raise HTTPException(status_code = 400, detail = "Failed to update user.")
            
@router.get("/{account_id}")
def get_account(id: int):
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            "SELECT id, first_name, last_name, age, weight, height FROM accounts WHERE id = :id"),
            { "id": id}
        )

        res = result.mappings().first()

        if res:
            return {
                "first_name": res.first_name,
                "last_name": res.last_name,
                "age": res.age,
                "weight": res.weight,
                "height": res.height
            }

    raise HTTPException(status_code = 404, detail = "Invalid Account.")
     
@router.get("/{account_id}/recipes")
def get_account(id: int):
    try:
        with db.engine.begin() as connection:
            validate_user = connection.execute(sqlalchemy.text("""SELECT 1 FROM accounts WHERE id = :account_id"""), {"account_id": id}).one_or_none()

            if validate_user is None:
                raise Exception("Account not found.")

            result = connection.execute(sqlalchemy.text(
                "SELECT recipes.id, recipes.name FROM recipes WHERE author_id = :id"),
                { "id": id}
            )

            res = result.mappings().all()

            if res:
                return res
            else:
                raise Exception("Account is not the author of any recipes.")
    except Exception as e:
        return HTTPException(status_code = 404, detail = f"Error: {e}")

@router.get("/{account_id}/meal-plans")
def get_meal_plans(account_id: int):
    try:
        with db.engine.begin() as connection:
            validate_user = connection.execute(sqlalchemy.text("""SELECT 1 FROM accounts WHERE id = :account_id"""), {"account_id": account_id}).one_or_none()

            if validate_user is None:
                raise Exception("Account not found.")

            results = connection.execute(sqlalchemy.text("""SELECT id, name, description
                                            FROM meal_plans
                                            WHERE author_id = :account_id 
                                            UNION 
                                            SELECT meal_plan_id, name, description FROM shared_meal_plans 
                                            JOIN meal_plans ON shared_meal_plans.meal_plan_id = meal_plans.id 
                                            WHERE recipient_id = :account_id"""), {"account_id": account_id}).mappings().all()
        
            if results:
                return results
            else:
                raise Exception("Account is not the author of any meal plans.")

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"{e}")