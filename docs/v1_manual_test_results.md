# Example workflow

John owns a restaurant, and wants somewhere to store the nutrition facts about one of his meals. John already has an account, so to save his recipe he:

-   Sends a POST request to `/recipes/create`, where he supplies some general info about the recipe (such as name and how many people it serves). In response, he receives a recipe id of `1234`.
-   He then sends a POST request to `/recipes/1234` with a list of ingredients and their quantities.
-   When he wants to retrieve his recipe, he send a GET request to `/recipes/1234`, where the recipe info is provided for him.

# Testing results

1: Creating the recipe (request)

    curl -X 'POST'
    'http://127.0.0.1:3000/recipes/create'
    -H 'accept: application/json'
    -H 'Content-Type: application/json'
    -d '{
            "author_id": 1,
            "name": "John'\''s Famous Recipe",
            "servings": 1
        }'

2: (response)

    {
        "id": 11
    }

3: Adding an ingredient (request)

    curl -X 'POST' \
    'http://127.0.0.1:3000/recipes/11' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
            "ingredient_id": 1121821,
            "quantity": 4
        }'

4: (response)

    {
        "success": true
    }

5: Getting the recipe (request)

    curl -X 'GET' \
    'http://127.0.0.1:3000/recipes/11' \
    -H 'accept: application/json'

6: (response)

    {
        "name": "John's Famous Recipe",
        "created_by": 1,
        "servings": 1,
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
