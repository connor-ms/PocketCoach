from fastapi import FastAPI, exceptions
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from src.api import accounts, calories, ingredient, meal_plan, recipe, user
import json
import logging
import sys

description = """
Pocket Coach is the food tracking app that fits in your pocket!
"""

app = FastAPI(
    title="Pocket Coach",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Seth Langel",
        "email": "slangel@calpoly.edu",
    },
)

app.include_router(accounts.router)
app.include_router(calories.router)
app.include_router(ingredient.router)
app.include_router(meal_plan.router)
app.include_router(recipe.router)
app.include_router(user.router)

@app.exception_handler(exceptions.RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logging.error(f"The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}
    for error in exc_json:
        response['message'].append(f"{error['loc']}: {error['msg']}")

    return JSONResponse(response, status_code=422)

@app.get("/")
async def root():
    return {"message": "Welcome to the Pocket Coach."}
