# User Stories

1. As someone trying to lose weight, I want to view my daily calorie intake so I can monitor my diet.
2. As a runner, I want to be able to log my runs to track my calories burned.
3. As a restaurant owner, I want to be able to log the calorie count of my recipes.
4. As a personal chef, I want to be able to save my favorite recipes.

# Exceptions

1. The user provides an unrealistic daily caloric goal (ex: 500 calories/day).
    - The service will alert the user that it's an unsafe daily goal, and will suggest the lowest safe goal.
2. The user attempts to log an unexpected exercise type (ex: they make a typo, and enter "runing" instead of "running").
    - The service will alert the user that an unsupported exercise type was submitted, and will let the user know what exercies are allowed.
3. An ingredient has missing information and is used in a recipe.

    - The service will alert that there's missing macros, so the net total will be inaccurate.

    OR (not sure which is better, lmk?)

    - The service will not provide net totals for any macro that is missing in any ingredient, but it will still provide a net total for any macros that exist in all ingredients.

4. The user attempts to delete an ingredient that's being used in a recipe.
    - The service prevents deletion of any ingredient until it's not referenced in a recipe. It will alert what recipe(s) the ingredient is being used in.
