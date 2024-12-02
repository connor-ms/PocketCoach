import csv
from datetime import timedelta, timezone
import random
import sqlalchemy
import os
import dotenv
from faker import Faker
import numpy as np

def database_connection_url():
    dotenv.load_dotenv()

    return os.environ.get("POSTGRES_URI")

engine = sqlalchemy.create_engine(database_connection_url(), use_insertmanyvalues=True)

with engine.begin() as conn:
    conn.execute(sqlalchemy.text("""
    DROP TABLE IF EXISTS accounts CASCADE;
    DROP TABLE IF EXISTS calories CASCADE;
    DROP TABLE IF EXISTS meal_plans CASCADE;
    DROP TABLE IF EXISTS menustat CASCADE;
    DROP TABLE IF EXISTS plans_recipes CASCADE;
    DROP TABLE IF EXISTS recipe_ingredients CASCADE;
    DROP TABLE IF EXISTS recipes CASCADE;
    DROP TABLE IF EXISTS shared_meal_plans CASCADE;
    DROP TABLE IF EXISTS usda_branded CASCADE;
                                 
    create table
    public.accounts (
    id bigint generated by default as identity not null,
    age integer not null,
    weight integer null,
    height integer null,
    created_at timestamp with time zone null default now(),
    first_name text null,
    last_name text null,
    constraint account_pkey primary key (id)
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
                                 
    create table
  public.calories (
    id bigint generated by default as identity not null,
    calories real not null,
    created_at timestamp,
    account_id bigint null,
    constraint calories_pkey primary key (id),
    constraint calories_account_id_fkey foreign key (account_id) references accounts (id)
  ) tablespace pg_default;
                                 
    create table
  public.meal_plans (
    id bigint generated by default as identity not null,
    author_id bigint null,
    name text null,
    description text null,
    created_at timestamp with time zone not null default now(),
    constraint meal_plan_pkey primary key (id),
    constraint meal_plan_author_id_fkey foreign key (author_id) references accounts (id)
  ) tablespace pg_default;

    create table
  public.plans_recipes (
    id bigint generated by default as identity not null,
    meal_plan_id bigint null,
    recipe_id bigint null,
    created_at timestamp with time zone not null default now(),
    constraint plans_recipes_pkey primary key (id),
    constraint plans_recipes_meal_plan_id_fkey foreign key (meal_plan_id) references meal_plans (id),
    constraint plans_recipes_recipe_id_fkey foreign key (recipe_id) references recipes (id)
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
  public.shared_meal_plans (
    id bigint generated by default as identity not null,
    meal_plan_id bigint null,
    recipient_id bigint null,
    created_at timestamp with time zone not null default now(),
    constraint shared_meal_plans_pkey primary key (id),
    constraint shared_meal_plans_meal_plan_id_fkey foreign key (meal_plan_id) references meal_plans (id),
    constraint shared_meal_plans_recipient_id_fkey foreign key (recipient_id) references accounts (id)
  ) tablespace pg_default;
                                 
    create table
  public.usda_branded (
    fdc_id bigint generated by default as identity not null,
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
    cholesterol_amount double precision null,
    cholesterol_unit text null,
    vitamin_c_total_ascorbic_acid_amount double precision null,
    vitamin_c_total_ascorbic_acid_unit text null,
    vitamin_d_d2_d3_international_units_amount double precision null,
    vitamin_d_d2_d3_international_units_unit text null,
    vitamin_a_iu_amount double precision null,
    vitamin_a_iu_unit text null,
    sodium_amount double precision null,
    sodium_na_unit text null,
    potassium double precision null,
    potassium_unit text null,
    iron_amount double precision null,
    iron_fe_unit text null,
    calcium_ca_amount text null,
    calcium_ca_unit text null,
    fiber_amount text null,
    fiber_unit text null,
    calories_amount double precision null,
    calorie_unit text null,
    carb_amount double precision null,
    carb_unit text null,
    fat_amount double precision null,
    fat_unit text null,
    protein_amount double precision null,
    protein_unit text null,
    constraint test3_pkey primary key (fdc_id)
    ) tablespace pg_default;
    """))

num_users = 200000
fake = Faker()
calories_posts_sample_distribution = np.random.default_rng().negative_binomial(0.04, 0.01, num_users)
total_posts = 0

def try_convert(value):
    if value == "":
        return None
    
    try:
        int_value = int(value)
        return int_value
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value

# import real food data
with engine.begin() as conn:
    to_insert = []
    file_name = "data/usda_branded_500k.csv"
    BATCH_SIZE = 7000

    try:
        with open(file_name, 'r', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.DictReader(csvfile)

            for line_number, row in enumerate(csvreader, start=2):
                try:
                    converted_row = { key: try_convert(value) for key, value in row.items() }
                    del converted_row["fdc_id"]
                    print(converted_row)
                    # id = conn.execute(sqlalchemy.text("""
                    # INSERT INTO usda_branded (*) VALUES (:description, :brand_name, :brand_owner, :ingredients, :serving_size, :serving_size_unit, :food_category, :update_year, :sugars_total_including_nlea_amount, :sugars_total_including_nlea_unit, :fatty_acids_total_saturated_amount, :fatty_acids_total_saturated_unit, :cholesterol_amount, :cholesterol_unit, :vitamin_c_total_ascorbic_acid_amount, :vitamin_c_total_ascorbic_acid_unit, :vitamin_d_d2_d3_international_units_amount, :vitamin_d_d2_d3_international_units_unit, :vitamin_a_iu_amount, :vitamin_a_iu_unit, :sodium_na_amount, :sodium_na_unit, :potassium_amount, :potassium_unit, :iron_fe_amount, :iron_fe_unit, :calcium_ca_amount, :calcium_ca_unit, :fiber_amount, :fiber_unit, :energy_amount, :energy_unit, :carb_amount, :carb_unit, :fat_amount, :fat_unit, :protein_amount, :protein_unit) RETURNING id;
                    # """), converted_row).scalar_one()
                    # to_insert.append(converted_row)

                    # if len(to_insert) >= BATCH_SIZE:
                    #     try:
                            
                    #         print(f"Inserted {len(to_insert)} rows.")
                    #         to_insert.clear()
                    #     except Exception as e:
                    #         print(f"Error inserting data: {e}")

                except Exception as e:
                    print(f"Error on line {line_number}")
                    print(f"Error details: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")

# create fake accounts and calorie logs
with engine.begin() as conn:
    posts = []
    for i in range(num_users):
        if (i % 10 == 0):
            print(i)
        
        name = fake.name().split(' ')
        first = name[0]
        last = name[1]
        age = np.random.randint(12,101)
        weight = np.random.randint(80, 451)
        height = np.random.randint(50, 101)

        id = conn.execute(sqlalchemy.text("""
        INSERT INTO accounts (age, weight, height, first_name, last_name) VALUES (:age, :weight, :height, :first, :last) RETURNING id;
        """), {"age": age, "first": first, "last": last, "weight": weight, "height": height}).scalar_one()

        num_posts = calories_posts_sample_distribution[i]

        for j in range(num_posts):
            fake_timestamp = fake.date_time_between(start_date="-4y", end_date="now")
            total_posts += 1
            posts.append({
                "account_id": id,
                "calories": np.random.randint(-2000, 2001),
                "created_at": fake_timestamp
            })
        
    if posts:
        conn.execute(sqlalchemy.text("""
        INSERT INTO calories (account_id, calories, created_at) 
        VALUES (:account_id, :calories, :created_at);
        """), posts)

    print("total posts: ", total_posts)