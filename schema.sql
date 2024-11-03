create table
  public.menustat (
    menustat_id bigint not null,
    restaurant text null,
    food_category text null,
    description text null,
    item_description text null,
    serving_size text null,
    serving_size_text text null,
    serving_size_unit text null,
    serving_size_household text null,
    energy_amount text null,
    fat_amount text null,
    saturated_fat_amount text null,
    trans_fat_amount text null,
    cholesterol_amount text null,
    sodium_amount text null,
    potassium_amount text null,
    carb_amount text null,
    protein_amount text null,
    sugar_amount text null,
    fiber_amount text null,
    energy_per_100g text null,
    fat_per_100g text null,
    saturated_fat_per_100g text null,
    trans_fat_per_100g text null,
    cholesterol_per_100g text null,
    sodium_per_100g text null,
    potassium_per_100g text null,
    carbs_per_100g text null,
    protein_per_100g text null,
    sugar_per_100g text null,
    dietary_fiber_per_100g text null,
    constraint menustat_pkey primary key (menustat_id)
  ) tablespace pg_default;

create table
  public.usda_branded (
    fdc_id bigint not null,
    description text null,
    brand_name text null,
    brand_owner text null,
    ingredients text null,
    serving_size double precision null,
    serving_size_unit text null,
    food_category text null,
    update_year bigint null,
    sugars_total_including_nlea_amount double precision null,
    sugars_total_including_nlea_unit text null,
    fatty_acids_total_saturated_amount double precision null,
    fatty_acids_total_saturated_unit text null,
    cholesterol_amount text null,
    cholesterol_unit text null,
    vitamin_c_total_ascorbic_acid_amount text null,
    vitamin_c_total_ascorbic_acid_unit text null,
    vitamin_d_d2_d3_international_units_amount text null,
    vitamin_d_d2_d3_international_units_unit text null,
    vitamin_a_iu_amount text null,
    vitamin_a_iu_unit text null,
    sodium_na_amount text null,
    sodium_na_unit text null,
    potassium_amount text null,
    potassium_unit text null,
    iron_fe_amount text null,
    iron_fe_unit text null,
    calcium_ca_amount text null,
    calcium_ca_unit text null,
    fiber_amount text null,
    fiber_unit text null,
    energy_amount double precision null,
    energy_unit text null,
    carb_amount text null,
    carb_unit text null,
    fat_amount double precision null,
    fat_unit text null,
    protein_amount text null,
    protein_unit text null,
    constraint usda_branded_pkey primary key (fdc_id)
  ) tablespace pg_default;

create table
  public.usda_non_branded (
    id bigint generated by default as identity not null,
    usda_data_type text null,
    description text null,
    update_year bigint null,
    serving_amount double precision null,
    serving_text text null,
    serving_size double precision null,
    protein_unit text null,
    carb_unit text null,
    fat_unit text null,
    energy_unit text null,
    protein_amount double precision null,
    fat_amount double precision null,
    carb_amount double precision null,
    energy_amount double precision null,
    fiber_amount double precision null,
    fiber_unit text null,
    potassium_amount double precision null,
    potassium_unit text null,
    fdc_id numeric null,
    constraint usda_non_branded_pkey primary key (id)
  ) tablespace pg_default;

create table
  public.recipe_ingredients (
    id bigint generated by default as identity not null,
    ingredient_id bigint not null,
    quantity bigint not null,
    recipe_id bigint not null,
    constraint recipe_ingredients_pkey primary key (id)
  ) tablespace pg_default;

create table
  public.recipes (
    id bigint generated by default as identity not null,
    author_id bigint not null,
    name text not null,
    servings bigint not null,
    created_at timestamp with time zone not null default now(),
    constraint recipes_pkey primary key (id)
  ) tablespace pg_default;
CREATE TABLE 
  public.meal_plans (
    id BIGINT GENERATED BY DEFAULT AS IDENTITY NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    daily_calorie_goal INT NOT NULL,
    CONSTRAINT meal_plans_pkey PRIMARY KEY (id)
) TABLESPACE pg_default;
CREATE TABLE 
  public.meal_logs (
    id BIGINT GENERATED BY DEFAULT AS IDENTITY NOT NULL,
    meal_plan_id BIGINT NOT NULL, 
    date DATE NOT NULL,
    recipe_id BIGINT NOT NULL,  
    quantity INT NOT NULL,
    meal_type TEXT NOT NULL, 
    CONSTRAINT meal_logs_pkey PRIMARY KEY (id),
    CONSTRAINT fk_meal_plan FOREIGN KEY (meal_plan_id) REFERENCES public.meal_plans(id),
    CONSTRAINT fk_recipe FOREIGN KEY (recipe_id) REFERENCES public.recipes(id)
) TABLESPACE pg_default;
