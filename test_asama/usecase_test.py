import database_test as database

class RecipeRequest:
    latitude: float
    longitude: float
    time: int

class Store:
    name:str
    latitude:str
    longitude:str
    items:list[str]

class Recipe:
    name:str
    time:str
    url:str
    stores:list[Store]
    def __init__(self, stores: list[Store]):
        self.stores = stores

class RecipeResponse:
    recipes: list[Recipe]
    def __init__(self, recipes: list[Recipe]):
        self.recipes = recipes

def get_dict_store_name_to_id():
    stores = database.get_store()
    store_name_to_id: dict[str, int] = {}
    for store in stores:
        store_name_to_id[store[1]] = store[0]
    return store_name_to_id

def get_dict_item_name_to_id():
    items = database.get_item()
    item_name_to_id: dict[str, int] = {}
    for item in items:
        item_name_to_id[item[1]] = item[0]
    return item_name_to_id

def add_items_by_name(store_name:str, items:list[tuple[str, int]]):
    store_name_to_id = get_dict_store_name_to_id()
    item_name_to_id = get_dict_item_name_to_id()
    store_id = store_name_to_id.get(store_name, -1)
    if store_id >= 0:
        for item in items:
            item_id = item_name_to_id.get(item[0], -1)
            if item_id < 0:
                item_id = database.add_item(item[0])
                item_name_to_id[item[0]] = item_id
            database.add_handling(store_id, item_id)

def add_stores(stores:list[tuple[str, float, float, str]]):
    store_name_to_id = get_dict_store_name_to_id()
    for store in stores:
        if store_name_to_id(stores[0]) >= 0:
            continue
        database.add_store(store[0], store[1], store[2], store[3])

def get_recipe():
    recipes = database.get_recipe()

def clear_item():
    database.clear_item()