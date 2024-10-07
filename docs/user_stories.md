# User Stories

1. As someone trying to lose weight, I want to view my daily calorie intake so I can monitor my diet.
2. As a runner, I want to be able to log my runs to track my calories burned.
3. As a restaurant owner, I want to be able to log the calorie count of my recipes.
4. As a personal chef, I want to be able to save my favorite recipes.
5. As a personal trainer, I want to be able to share meal plans with my clients.
6. As a diatition, I want to keep track of my clients intake.
7. As a person with dietary restrictions, I want to remove ingredients from all my food/recipe options.
8. As a person who wants to meal prep more, I want to be able to store recipes with the nutritional facts.

# Exceptions

1. The user provides an unrealistic daily caloric goal (ex: 500 calories/day).
    - The service will alert the user that it's an unsafe daily goal, and will suggest the lowest safe goal.
2. The user attempts to log an unexpected exercise type (ex: they make a typo, and enter "runing" instead of "running").
    - The service will alert the user that an unsupported exercise type was submitted, and will let the user know what exercise types are allowed.
3. An ingredient has missing information and is used in a recipe.

    - The service will alert that there's missing macros, so the net total will be inaccurate.

    OR (not sure which is better, lmk?)

    - The service will not provide net totals for any macro that is missing in any ingredient, but it will still provide a net total for any macros that exist in all ingredients.

4. The user attempts to delete an ingredient that's being used in a recipe.
    - The service prevents deletion of any ingredient until it's not referenced in a recipe. It will alert what recipe(s) the ingredient is being used in.

5. The user tries to share a meal plan with another user.
    - The service prevents the receiving user to import the new meal plan due to conflicting micro/macro goals. It will alert the receiving user of new micro/macro goals and if they are          okay with the changes
  
6. The user tries to view another users intake.
    - The service prevents this and prompts the initial user to send a request to the receiving user asking permission to view intake for a range in time.
  
7. The user tries to add a recipe that includes a ingredient that they added to their blacklist.
    - The service will alert the user of the ingredient and give them the option to still add the recipe or to cancel the action.
  
8. Ther user tries to add a recipe into their digital cookbook but has missing nutritional information.
    - The service will alert the user what information is missing and prompt them to add the info if they wish.
  
   
