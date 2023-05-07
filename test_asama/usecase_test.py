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

# 店名からDBに登録されているidを求める辞書を返す
def get_dict_store_name_to_id():
    stores = database.get_store()
    store_name_to_id: dict[str, int] = {}
    for store in stores:
        store_name_to_id[store[1]] = store[0]
    return store_name_to_id

# 特売の商品名からDBに登録されているidを求める辞書を返す
def get_dict_item_name_to_id():
    items = database.get_item()
    item_name_to_id: dict[str, int] = {}
    for item in items:
        item_name_to_id[item[1]] = item[0]
    return item_name_to_id

# 特売商品をDBに追加する
def add_items(store_name:str, items:list[tuple[str, int]]):
    item_name_to_id = get_dict_item_name_to_id()
    stores = database.get_store(name=store_name)
    if len(stores)>0:
        store_id = stores[0][0]
        for item in items:
            item_id = item_name_to_id.get(item[0], -1)
            if item_id < 0:
                item_id = database.add_item(item[0])
                item_name_to_id[item[0]] = item_id
            database.add_handling(store_id, item_id)

# 店をDBに追加する
def add_stores(stores:list[tuple[str, float, float, str]]):
    store_name_to_id = get_dict_store_name_to_id()
    for store in stores:
        if store_name_to_id(stores[0]) >= 0:
            continue
        database.add_store(store[0], store[1], store[2], store[3])

# 最適なレシピを求める
def get_recipe():
    recipes = database.get_recipe()

# 特売商品情報をリセットする
def clear_item():
    database.clear_item_table()