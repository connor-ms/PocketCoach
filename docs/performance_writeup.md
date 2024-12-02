# Fake Data Modeling

Here are the totals of data we faked, with the exception of ingredients. Ingredients include real data, as our sample data was well over 1,000,000 rows. We only imported 100k to leave room for fake data elsewhere.

-   Accounts: 200k
-   Calories: ~800k
-   Meal plans: 200k
-   Plans_recipes: ~800k
-   Recipes: 200k
-   Recipe_ingredients: ~800k
-   Ingredients: 100k

We think it would scale this way as there will be much more data logged for calorie intake/outtake, so it makes sense for there to be many more calorie entries than accounts. It's a similar idea for meal plans and adding recipes, as well as adding ingredients to recipes. Ingredients won't scale much, as there won't be many cases where custom ingredients need to be made. In a normal database, this would have the full dataset of ~1.5 million rows.

Our data generation is located in `data/fake_data.py`.

## Timings

### Accounts:

-   Create: 0.0105s
-   Update: 0.0114s
-   Get: 0.0249s
-   Get account recipe: 0.05s

### Calories:

-   Log: 0.0207s
-   Get: 0.1386s

### Ingredients:

-   Create: 0.008s
-   Update: 0.019s
-   Delete: 0.0148s
-   Get by id: 0.0147s
-   Get by name: 0.0735s

### Recipes:

-   Create: 0.0468s
-   Adding ingredient to recipe: 0.0313s
-   Retrieve: 0.0975s

### Meal Plans

-   Create: 0.0246s
-   Get: 0.0929s
-   Delete: 0.0983s
-   Add recipe: 0.0033s
-   Remove recipe: 0.1015s
-   Share: 0.0089s
-   Stats: 0.253s

## Three slowest:

-   Meal plan stats: 0.253s - added index on author_id -> new time is 0.162s

Query planner:

```
[
  {
    "QUERY PLAN": "GroupAggregate  (cost=28057.42..28556.05 rows=3239 width=52) (actual time=241.807..243.572 rows=1 loops=1)"
  },
  {
    "QUERY PLAN": "  Group Key: r.name"
  },
  {
    "QUERY PLAN": "  ->  Nested Loop  (cost=28057.42..28483.17 rows=3239 width=52) (actual time=241.075..243.407 rows=2025 loops=1)"
  },
  {
    "QUERY PLAN": "        ->  Gather Merge  (cost=28057.00..28434.24 rows=3239 width=52) (actual time=241.054..242.946 rows=2025 loops=1)"
  },
  {
    "QUERY PLAN": "              Workers Planned: 2"
  },
  {
    "QUERY PLAN": "              Workers Launched: 2"
  },
  {
    "QUERY PLAN": "              ->  Sort  (cost=27056.98..27060.36 rows=1350 width=52) (actual time=230.408..230.447 rows=675 loops=3)"
  },
  {
    "QUERY PLAN": "                    Sort Key: r.name"
  },
  {
    "QUERY PLAN": "                    Sort Method: quicksort  Memory: 25kB"
  },
  {
    "QUERY PLAN": "                    Worker 0:  Sort Method: quicksort  Memory: 189kB"
  },
  {
    "QUERY PLAN": "                    Worker 1:  Sort Method: quicksort  Memory: 25kB"
  },
  {
    "QUERY PLAN": "                    ->  Nested Loop  (cost=14805.99..26986.79 rows=1350 width=52) (actual time=227.377..230.268 rows=675 loops=3)"
  },
  {
    "QUERY PLAN": "                          ->  Parallel Hash Join  (cost=14805.70..26513.64 rows=1350 width=28) (actual time=227.364..229.401 rows=675 loops=3)"
  },
  {
    "QUERY PLAN": "                                Hash Cond: (pr.recipe_id = ri.recipe_id)"
  },
  {
    "QUERY PLAN": "                                ->  Nested Loop  (cost=0.42..10085.43 rows=21 width=36) (actual time=21.082..31.450 rows=15 loops=3)"
  },
  {
    "QUERY PLAN": "                                      ->  Parallel Seq Scan on plans_recipes pr  (cost=0.00..9911.60 rows=21 width=16) (actual time=21.060..31.409 rows=15 loops=3)"
  },
  {
    "QUERY PLAN": "                                            Filter: (meal_plan_id = 1234)"
  },
  {
    "QUERY PLAN": "                                            Rows Removed by Filter: 262999"
  },
  {
    "QUERY PLAN": "                                      ->  Index Scan using recipes_pkey on recipes r  (cost=0.42..8.28 rows=1 width=20) (actual time=0.002..0.002 rows=1 loops=45)"
  },
  {
    "QUERY PLAN": "                                            Index Cond: (id = pr.recipe_id)"
  },
  {
    "QUERY PLAN": "                                ->  Parallel Hash  (cost=9089.68..9089.68 rows=328768 width=16) (actual time=181.466..181.467 rows=263014 loops=3)"
  },
  {
    "QUERY PLAN": "                                      Buckets: 262144  Batches: 8  Memory Usage: 6976kB"
  },
  {
    "QUERY PLAN": "                                      ->  Parallel Seq Scan on recipe_ingredients ri  (cost=0.00..9089.68 rows=328768 width=16) (actual time=0.625..97.652 rows=263014 loops=3)"
  },
  {
    "QUERY PLAN": "                          ->  Index Scan using test3_pkey on usda_branded i  (cost=0.29..0.35 rows=1 width=40) (actual time=0.001..0.001 rows=1 loops=2025)"
  },
  {
    "QUERY PLAN": "                                Index Cond: (id = ri.ingredient_id)"
  },
  {
    "QUERY PLAN": "        ->  Materialize  (cost=0.42..8.44 rows=1 width=8) (actual time=0.000..0.000 rows=1 loops=2025)"
  },
  {
    "QUERY PLAN": "              ->  Index Only Scan using meal_plan_pkey on meal_plans mp  (cost=0.42..8.44 rows=1 width=8) (actual time=0.015..0.016 rows=1 loops=1)"
  },
  {
    "QUERY PLAN": "                    Index Cond: (id = 1234)"
  },
  {
    "QUERY PLAN": "                    Heap Fetches: 0"
  },
  {
    "QUERY PLAN": "Planning Time: 7.274 ms"
  },
  {
    "QUERY PLAN": "Execution Time: 89.688 ms"
  }
]
```

-   Get calories: 0.1386s - added index on account_id -> new time is 0.084s

Query planner:

```
[{'QUERY PLAN': 'Delete on plans_recipes  (cost=0.42..9.43 rows=0 width=0) (actual time=0.019..0.019 rows=0 loops=1)'}, {'QUERY PLAN': '  ->  Index Scan using meal_plan_remove_index on plans_recipes  (cost=0.42..9.43 rows=1 width=6) (actual time=0.008..0.009 rows=1 loops=1)'}, {'QUERY PLAN': '        Index Cond: (recipe_id = 123)'}, {'QUERY PLAN': '        Filter: (meal_plan_id = 20000)'}, {'QUERY PLAN': 'Planning Time: 0.045 ms'}, {'QUERY PLAN': 'Execution Time: 0.151 ms'}]
```

-   Meal plan remove recipe: 0.1015s - added index on recipe_id, meal_plan_id -> 0.003s

Query planner:

```
[{'QUERY PLAN': 'Finalize GroupAggregate  (cost=12555.99..12562.00 rows=49 width=36) (actual time=22.989..23.929 rows=45 loops=1)'}, {'QUERY PLAN': "  Group Key: (to_char(date_trunc('day'::text, created_at), 'YYYY-MM-DD'::text))"}, {'QUERY PLAN': '  ->  Gather Merge  (cost=12555.99..12561.06 rows=40 width=36) (actual time=22.985..23.903 rows=45 loops=1)'}, {'QUERY PLAN': '        Workers Planned: 2'}, {'QUERY PLAN': '        Workers Launched: 2'}, {'QUERY PLAN': '        ->  Partial GroupAggregate  (cost=11555.97..11556.42 rows=20 width=36) (actual time=20.812..20.816 rows=15 loops=3)'}, {'QUERY PLAN': "              Group Key: (to_char(date_trunc('day'::text, created_at), 'YYYY-MM-DD'::text))"}, {'QUERY PLAN': '              ->  Sort  (cost=11555.97..11556.02 rows=20 width=36) (actual time=20.809..20.810 rows=15 loops=3)'}, {'QUERY PLAN': "                    Sort Key: (to_char(date_trunc('day'::text, created_at), 'YYYY-MM-DD'::text))"}, {'QUERY PLAN': '                    Sort Method: quicksort  Memory: 26kB'}, {'QUERY PLAN': '                    Worker 0:  Sort Method: quicksort  Memory: 25kB'}, {'QUERY PLAN': '                    Worker 1:  Sort Method: quicksort  Memory: 25kB'}, {'QUERY PLAN': '                    ->  Parallel Seq Scan on calories  (cost=0.00..11555.54 rows=20 width=36) (actual time=13.396..20.754 rows=15 loops=3)'}, {'QUERY PLAN': "                          Filter: ((created_at >= '2020-12-01'::date) AND (created_at <= '2024-12-01'::date) AND (account_id = 1234))"}, {'QUERY PLAN': '                          Rows Removed by Filter: 262999'}, {'QUERY PLAN': 'Planning Time: 0.097 ms'}, {'QUERY PLAN': 'Execution Time: 23.954 ms'}]
```
