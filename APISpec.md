# API Specifications for PocketCoach

## 1. Account

The API calls are made in this sequence when creating and editing an account:

1. `Register User`
2. `Update Account`

### 1.1. Register Account `/user` (POST)

Creates the account of the user with the following information.

**Request**:

```json
{
    "age": "integer" /* Between 15 and 60 years */,
    "weight": "integer" /* Between 50 and 1000 pounds*/,
    "height": "integer" /* Between 48 and 108 inches*/
}
```

**Response**:

```json
{
    "user_id": "integer"
}
```

### 1.2. Update Account - `/user` (PUT)

Updates the users information.

**Request**:

```json
{
    "user_id": "integer",
    "age": "integer",
    "weight": "integer",
    "height": "integer"
}
```

**Response**:

```json
{
    "success": "boolean"
}
```

## 2. Ingredients

The API calls are made in this sequence when the ingredients comes:

1. `Create Custom Ingredient`
2. `Update Custom Ingredient`
3. `Delete Custom Ingredient`
4. `Retrieve Ingredient`
5. `Retrieve Ingredients`

### 2.1. Create Custom Ingredient - `/ingredient` (POST)

Creates a new custom ingredient for that user.

**Request**:

```json
{
    "name": "string",
    "serving_size_type": "string",
    "serving_size": "integer",
    "calories": "integer"
}
```

### 2.2. Update Custom Ingredient - `/ingredient/{ingredient_id}` (PUT)

Updates a single ingredient.

**Request**:

```json
{
    "name": "string",
    "serving_size_type": "string",
    "serving_size": "integer",
    "calories": "integer"
}
```

### 2.3. Deletes Custom Ingredient - `/ingredient/{ingredient_id}` (DELETE)

Deletes ingredient.

**Response**:

```json
{
    "success": "boolean"
}
```

### 2.4. Retrieve Ingredient - `/ingredient/{ingredient_id}` (GET)

Retrieves a single ingredient.

**Response**:

```json
{
    "id": "integer",
    "name": "string",
    "serving_size_type": "string",
    "serving_size": "integer",
    "calories": "integer"
}
```

### 2.5. Retrieves all Ingredients - `/ingredient` (GET)

Retrieves all ingredients.

**Response**:

```json
[
    {
        "id": "integer",
        "name": "string",
        "serving_size_type": "string",
        "serving_size": "integer",
        "calories": "integer"
    },
    ...
]
```

## 3. Recipes

### 3.1. Create Custom Recipe - `/recipe/create` (POST)

Creates an empty recipe.

**Request**:

```json
{
    "author_id": "integer",
    "name": "string",
    "servings": "integer"
}
```

**Response**:

```json
{
    "id": "integer"
}
```

### 3.2. Edit Recipe - `/recipe/{recipe_id}` (PUT)

Edits an existing recipe.

**Request**:

```json
{
    "name": "string",
    "servings": "integer"
}
```

### 3.3. Delete Recipe - `/recipe/{recipe_id}` (DELETE)

Deletes an existing recipe. The recipe will only be deleted if `user_id` matches the recipe's `author_id`.

**Request**:

```json
{
    "user_id": "integer"
}
```

### 3.4. Add Ingredient(s) to Recipe - `/recipe/{recipe_id}` (POST)

Adds one or more ingredients to a recipe.

**Request**:

```json
[
    {
        "ingredient_id": "integer",
        "quantity": "integer",
    },
    ...
]
```

### 3.5. Remove Ingredient from Recipe - `/recipe/{recipe_id}` (DELETE)

Removes one or more ingredients from a recipe.

**Request**:

```json
[
    {
        "ingredient_id": "integer"
    },
    ...
]
```

### 3.6. Retrieve Recipe - `/recipe/{recipe_id}` (GET)

Retrieves a recipe.

**Response**:

```json
{
    "name": "string",
    "created_by": "integer",
    "servings": "integer",
    "ingredients": [
        {
            // /ingredient/{ingredient_id} response
        },
        ...
    ],
    "net_calories": "integer",
    "net_protein": "integer",
    "net_carbs": "integer"
}
```

### 4. Meal Plan

### 4.1.Create Meal Plan - /meal-plan (POST)

**Request**:

Create a plan for a specific user

```json
{
    "user_id": "integer",
    "name": "string",
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD",
    "daily_calorie_goal": "number"
}
```

**Response**:

```json
{
    "meal_plan_id": "integer"
}
```

### 4.2. Add Recipe to Meal Plan - /meal-plan/{meal_plan_id}/recipe (POST)

```json
{
    "date": "YYYY-MM-DD",
    "meal_type": "string", // e.g., breakfast, lunch
    "recipe_id": "integer",
    "servings": "integer"
}
```

**Response**:

```json
{
    "message": "Recipe added successfully."
}
```

### 4.3. Edit Meal Plan - /meal-plan/{meal_plan_id} (PUT)

Edit the details of an existing meal plan (name, dates, calorie goal).

```json
{
    "name": "string",
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD",
    "daily_calorie_goal": "number"
}
```

### 4.4. Delete Meal Plan - /meal-plan/{meal_plan_id} (DELETE)

Delete an existing meal plan.

**Response**:

```json
{
    "message": "Meal plan deleted successfully."
}
```

### 4.5. Get Meal Plan - /meal-plan/{meal_plan_id} (GET)

Retrieve details of a specific meal plan.

**Response**:

```json
{
    "meal_plan_id": "integer",
    "name": "string",
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD",
    "daily_calorie_goal": "number",
    "meals": [
        {
            "date": "YYYY-MM-DD",
            "meal_type": "string",
            "recipes": [
                {
                    "recipe_id": "integer",
                    "name": "string",
                    "calories": "number"
                }
            ]
        }
    ],
    "total_calories": "number"
}
```

### 4.6. List All Meal Plans - /user/{user_id}/meal-plan (GET)

Retrieve all meal plans for a specific user.

**Response**:

```json
[
    {
        "meal_plan_id": "integer",
        "name": "string",
        "start_date": "YYYY-MM-DD",
        "end_date": "YYYY-MM-DD"
    }
]
```

### 5. Calories

### 5.1. Calorie Intake - `calorie/intake` (POST)

Return a summary of your meal plan calorie total.

**Response**:

```json
{
    "number_of_calories": "number",
)
```

### 5.2 Calories Burned - `calorie/burn` (POST)

Return a summary of the amount of calories burned which is your intake minus your exercise input

**Response**:

```json
{
    "calories_burned": "number"
}
```
