import csv
from db_model import (
    session,
    Store,
    Item,
    Handling,
    Recipe,
    Ingredient,
    Need
)

def database_init():
    input_store_from_csv(session)
    input_recipe_from_csv(session)
    print_all_store(session)

def input_store_from_csv(session):
    session.query(Store).delete()
    session.query(Item).delete()
    session.query(Handling).delete()

    filename = "test_asama/db_store.csv"
    with open(filename, encoding='shift-jis', newline='') as f:
        csvreader = csv.reader(f)
        header = next(csvreader)
        stores = []
        for row in csvreader:
            stores.append(Store(
                name = row[0],
                latitude = float(row[1]),
                longitude = float(row[2]),
                flyer_url = row[3]
            ))
        session.add_all(stores)
        session.commit()

def input_recipe_from_csv(session):

    session.query(Recipe).delete()
    session.query(Ingredient).delete()
    session.query(Need).delete()
    recipe_list = []

    ingredient_name_to_id: dict[str, int] = {}

    filename = "test_asama/db_recipe.csv"
    with open(filename, encoding='shift-jis', newline='') as f:
        csvreader = csv.reader(f)
        header = next(csvreader)
        for row in csvreader:
            ingredient_list = row[3].split(';')
            recipe_list.append([row[0],row[1],row[2],ingredient_list,0])
            for ingredient in ingredient_list:
                ingredient_name_to_id[ingredient] = 0

    # Ingredient(材料)を追加
    for ingredient_name in ingredient_name_to_id.keys():
        ingredient = Ingredient(name=ingredient_name)
        session.add(ingredient)
        session.commit()
        ingredient_name_to_id[ingredient_name] = ingredient.id

    # Recipe(レシピ)を追加
    for i,recipe_detail in enumerate(recipe_list):
        recipe = Recipe(name=recipe_detail[0], time=recipe_detail[1], url=recipe_detail[2])
        session.add(recipe)
        session.commit()
        recipe_list[i][4] = recipe.id

    # Need(レシピに必要な材料情報)を追加
    add_needs = []
    for recipe_detail in recipe_list:
        recipe_id = recipe_detail[4]
        for ingredient in recipe_detail[3]:
            ingredient_id = ingredient_name_to_id[ingredient]
            add_needs.append(Need(recipe_id=recipe_id, ingredient_id=ingredient_id))
    session.add_all(add_needs)
    session.commit()

def print_all_store(session):
    stores = session.query(Store).all()
    for store in stores:
        print(store.name)


if __name__ == '__main__':
    database_init()