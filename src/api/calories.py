from datetime import date
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Response
from pydantic import BaseModel
import sqlalchemy
from datetime import datetime
from src import database as db

router = APIRouter(
    prefix="/calories",
    tags=["Calories"],
)

class Calories(BaseModel):
    account_id: int
    calorie_change: int

@router.post("/log")
def add_calorie_log(calories: Calories):
    """
    This endpoint accepts both positive and negative integers for both calories burned and gained. Limit for both is 4000 calories per call.
    """
    start=datetime.now()
    if calories.calorie_change > 4000:
        raise HTTPException(status_code = 400, detail = "Calories entered is too high. Calorie intake must be below 4000 calories.")
    elif calories.calorie_change < -4000:
        raise HTTPException(status_code=400, detail="Calories entered is too low. Calories burned must be above -4000 calories.")
    
    try:
        with db.engine.begin() as connection:
            account = connection.execute(sqlalchemy.text(
                "SELECT id FROM accounts WHERE id = :account_id"),
                {"account_id": calories.account_id }
            ).mappings().one_or_none()
            
            if account is None:
              raise Exception("Invalid account id. Please try and enter another id.")
        
            connection.execute(sqlalchemy.text(
                "INSERT INTO calories (account_id, calories) VALUES (:account_id ,:calories_change)"),
                { "calories_change": calories.calorie_change, "account_id": calories.account_id }
            )

            print(f"execution time: {datetime.now() - start}")
            return Response(status_code=200)
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")

@router.get("/")
def retrieve_calorie_total(account_id: int, start_date: Optional[date] = None, end_date: Optional[date] = None):
    """
        The calorie total for a specifc account can be retrieved in the following ways: \n
        1. If neither `start_date` nor `end_date` are provided, the endpoint will return all calorie totals by date. \n
        2. If both `start_date` and `end_date` are provided, the endpoint will return calorie totals by date within the given range. \n
        3. If only `start_date` is provided, the endpoint will return calorie totals by date starting from the given date, inclusive. \n
        4. If only `end_date` is provided, the endpoint will return calorie totals by date up to the given date, inclusive.\n
    """
    start=datetime.now()
    with db.engine.begin() as connection:
        sql_query = """
            SELECT
                TO_CHAR(DATE_TRUNC('day', created_at), 'YYYY-MM-DD') AS day,
                SUM(calories) AS total_calories
            FROM calories
            WHERE account_id = :account_id
        """
        
        params = {"account_id": account_id}
        
        if start_date:
            sql_query += " AND created_at >= :start_date"
            params["start_date"] = start_date
        
        if end_date:
            sql_query += " AND created_at <= :end_date"
            params["end_date"] = end_date
        
        sql_query += """
            GROUP BY day
            ORDER BY day
        """
        explain = "EXPLAIN ANALYZE " + sql_query
        results = connection.execute(sqlalchemy.text(sql_query), params)

        explain_result = connection.execute(sqlalchemy.text(explain), params).mappings().all()

        print(explain_result)
        print(f"execution time: {datetime.now() - start}")
        return results.mappings().all()