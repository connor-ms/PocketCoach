from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

import sqlalchemy
from src import database as db


router = APIRouter(
    prefix="/recipes",
    tags=["Recipe"],
)


class Recipe(BaseModel):
    author_id: Optional[int] = None
    name: Optional[str] = None
    servings: Optional[int] = None


@router.post("/create")
def create_recipe(recipe: Recipe):
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            "INSERT INTO recipes (author_id, name, servings) VALUES (:id, :name, :servings) RETURNING id"),
            { "id": recipe.author_id, "name": recipe.name, "servings": recipe.servings }
        )

        return result.mappings().one()  

    raise HTTPException(status_code=400, detail="Failed to create user.")