The get_daily_calories endpoint addresses concurrency issues such as phantom reads and non-repeatable reads. When calculating the total calories consumed on a specific day, concurrent transactions may add or modify meal entries, potentially leading to inaccurate results. Phantom reads occur when new records are added during the calculation, altering the totals unexpectedly. Similarly, non-repeatable reads happen if calorie counts are updated during the process.

The get_recipe endpoint demonstrates the challenges of non-repeatable reads. This issue arises when retrieving a recipe and its associated ingredients while another transaction updates the same data. For example, a recipe’s details or ingredients might change between reads, resulting in inconsistencies in the retrieved information.

The create_meal_plan endpoint focuses on preventing conflicts using the SERIALIZABLE isolation level. When multiple users attempt to create meal plans simultaneously, overlapping or conflicting entries can occur without proper safeguards. By applying the SERIALIZABLE isolation level, transactions are processed as though they occur sequentially, eliminating risks of conflicts.

#1

```mermaid
sequenceDiagram
    participant T1
    participant Database
    participant T2
    Note over T1, T2: The meal plan (id 1) has 3 meal entries, totalling 2350 calories for the day.
    T1->>Database: The net daily calories are requested
    T1->>Database: result = <a big query to sum up all calories for the day>.fetchone()[0]
    T2->>Database: Bob adds a meal to his meal plan.
    T2->>Database: INSERT INTO meal_logs (meal_plan_id, date, recipe_id, quantity, meal_type) VALUES (1, 9/14/24, 3, 1, "lunch")
    Note over T1, T2: The meal plan now has 4 meals.
    T1->>Database: The result is returned
    T1->>Database: return result
    Note over T1, T2: Bob has 4 meals logged (with a net total of 2600 calories), but was only shown 3 meals (with a net total of 2350 calories).
```

#2

```mermaid
sequenceDiagram
    participant S1 as Session 1
    participant DB as Database
    participant S2 as Session 2

    Note over S1, S2: Session 1 reads recipe and ingredients while Session 2 updates the recipe or ingredients.
    S1->>DB: SELECT * FROM recipes JOIN recipe_ingredients WHERE recipe_id = {recipe_id}
    DB-->>S1: Returns recipe and ingredient IDs
    S2->>DB: UPDATE recipes SET name = {new_name} WHERE id = {recipe_id}
    DB-->>S2: Confirm update
    S1->>DB: Call get_ingredient for each ingredient_id
    DB-->>S1: Returns updated ingredient data
    Note over S1: Recipe details in Session 1 are inconsistent with initial data.

```

#3

```mermaid
sequenceDiagram
    participant S1 as Session 1
    participant DB as Database
    participant S2 as Session 2

    Note over S1, S2: Session 1 and Session 2 attempt to create meal plans simultaneously.
    S1->>DB: INSERT INTO meal_plans (user_id, start_date, end_date, daily_calorie_goal)
    S2->>DB: INSERT INTO meal_plans (user_id, start_date, end_date, daily_calorie_goal)
    Note over DB: SERIALIZABLE isolation ensures one transaction is processed at a time.
    DB-->>S1: Confirm INSERT and return meal_plan_id
    DB-->>S2: Blocked until S1 completes
    S2->>DB: Retry or rollback depending on constraints
    DB-->>S2: Confirm INSERT or throw conflict error
    Note over S1, S2: Conflicts are avoided by sequential transaction processing.


```
