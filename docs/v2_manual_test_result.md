
# Example workflow

Bob is an avid gym-goer, and needs a way to make sure he's hitting his daily calorie and macro needs.
 To start off, he needs to create an account. He does this by sending a POST request to /user/create.
  He provides his height, weight, and age. He is then given his user ID, which he tattoos on his forearm so he never forgets it. All of the meals he normally eats already exist in the system, so he doesn't need to create any custom meals. Now that he has an account squared away,
 to create a meal plan he:

- Sends a POST request to /meal-plans. He wants to get back in shape for summer, so he provides a start date of 2024-01-01 and an end date of 2024-12-31. He wants to lose weight, so he specifes a daily goal of 2000 calories. In return he's given a meal plan ID of 1, which he tattoos on his belly so he can't forget it.

- He then logs a meal by sending a POST request to /meal-plan/meal-plans/1/log, where he specifies the date, recipe_id, quantity, and meal_type (e.g., "Lunch"). He receives a confirmation message: "Meal logged successfully".
- When he wants to check his daily calorie intake, he sends a GET request to /meal-plan/meal-plans/1/calories with a date query parameter (e.g., date=2024-11-03). In response, he receives the total calories for that date.


# Testing results

1: Creating the meal plan (request)
```
curl -X 'POST' \
  'http://127.0.0.1:8000/meal-plan/meal-plans' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": 1,
    "start_date": "2024-01-01",
    "end_date": "2024-12-31", 
    "daily_calorie_goal": 2000
}'
```
2: (response)
````
{
  "meal_plan_id": 1
}
    
    
````

3: Logging (request)

```
curl -X 'POST' \
  'http://127.0.0.1:8000/meal-plan/meal-plans/1/log' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "date": "2024-11-03",
  "recipe_id": 11,
  "quantity": 1,
  "meal_type": "Lunch"
}'
```
4: (response)

    {
        "message": "Meal Plan logged sucessfuly"
    }

5: Getting the recipe (request)
```
curl -X 'GET' \
  'http://127.0.0.1:8000/meal-plan/meal-plans/1/calories?date=2024-11-03' \
  -H 'accept: application/json'
```


6: (response)
```
{
  "date": "2024-11-03",
  "total_calories": 80.04
}
```
Bob feels like taking his diet to the extreme today, so he opted for 4 pickled sliced beets,which contributed to 80.04 calories.



   
        "ingredients": [
            {
                "fdc_id": 1121821,
                "description": "PICKLED SLICED BEETS",
                "brand_name": "",
                "brand_owner": "Tops Markets, LLC",
                "ingredients": "BEETS, WATER, HIGH FRUCTOSE CORN SYRUP, VINEGAR, SALT, NATURAL FLAVOR.",
                "serving_size": 29,
                "serving_size_unit": "g",
                "food_category": "Pickles, Olives, Peppers & Relishes",
                "update_year": 2020,
                "sugars_total_including_nlea_amount": 4,
                "sugars_total_including_nlea_unit": "G",
                "fatty_acids_total_saturated_amount": 0,
                "fatty_acids_total_saturated_unit": "G",
                "cholesterol_amount": "0.0",
                "cholesterol_unit": "MG",
                "vitamin_c_total_ascorbic_acid_amount": "0.0",
                "vitamin_c_total_ascorbic_acid_unit": "MG",
                "vitamin_d_d2_d3_international_units_amount": null,
                "vitamin_d_d2_d3_international_units_unit": "",
                "vitamin_a_iu_amount": "0.0",
                "vitamin_a_iu_unit": "IU",
                "sodium_na_amount": "55.1",
                "sodium_na_unit": "MG",
                "potassium_amount": "44.95",
                "potassium_unit": "MG",
                "iron_fe_amount": "0.0",
                "iron_fe_unit": "MG",
                "calcium_ca_amount": "0.0",
                "calcium_ca_unit": "MG",
                "fiber_amount": "0.0",
                "fiber_unit": "G",
                "energy_amount": 20.01,
                "energy_unit": "KCAL",
                "carb_amount": "4.0",
                "carb_unit": "G",
                "fat_amount": 0,
                "fat_unit": "G",
                "protein_amount": "0.0",
                "protein_unit": "G"
            }
        ]
    }
