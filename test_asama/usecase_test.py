import test_asama.database_test as database

class RecipeRequest:
    latitude: float
    longitude: float
    length: float
    time: int
    def __init__(self, latitude:float, longitude:float, length:float, time:int):
        self.latitude = latitude
        self.longitude = longitude
        self.length = length
        self.time = time

class Store:
    name:str
    latitude:str
    longitude:str
    flyer_url:str
    items:list[str]
    def __init__(self, name:str, latitude:float, longitude:float, flyer_url:str, items:list[str]):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.flyer_url = flyer_url
        self.items = items

class Recipe:
    name:str
    time:int
    url:str
    ingredients:list[str]
    stores:list[Store]
    def __init__(self, name:str, time:int, url:str, ingredients:list[str], stores: list[Store]):
        self.name = name
        self.time = time
        self.url = url
        self.ingredients = ingredients
        self.stores = stores

class RecipeResponse:
    recipes: list[Recipe]
    def __init__(self, recipes: list[Recipe]):
        self.recipes = recipes

class StoreInfoRequest:
    latitude: float
    longitude: float
    length: float
    def __init__(self, latitude:float, longitude:float, length:float):
        self.latitude = latitude
        self.longitude = longitude
        self.length = length

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
def get_recipe(request:RecipeRequest):
    store_info = get_store_info(
        StoreInfoRequest(
        latitude=request.latitude,
        longitude=request.longitude,
        length=request.length
    ))
    recipes = database.get_recipe()
    recipe_info_list = []
    for recipe in recipes:
        id = recipe[0]
        recipe_info_list.append(Recipe(
            name = recipe[1],
            time = recipe[2],
            url = recipe[3],
            ingredients = database.get_ingredient_names_by_recipe_id(id),
            stores = []
        ))
    return recipe_info_list

# 店名の一覧を求める
def get_store_names(request:StoreInfoRequest):
    stores = get_store_info(request)
    store_names = []
    for store in stores:
        store_names.append(store.name)
    return store_names

# 店名,緯度経度,扱っている特売商品名を求める
def get_store_info(request:StoreInfoRequest):
    stores = database.get_store(
        latitude=request.latitude,
        longitude=request.longitude,
        length=request.length
    )
    store_info_list = []
    for store in stores:
        id = store[0]
        store_info_list.append(Store(
            name = store[1],
            latitude = store[2],
            longitude = store[3],
            flyer_url = store[4],
            items = database.get_item_names_by_store_id(id)
        ))
    return store_info_list
def get_store_info_by_name(name:str):
    stores = database.get_store(name=name)
    if len(stores)>0:
        store = stores[0]
        id = store[0]
        return Store(
            name = store[1],
            latitude = store[2],
            longitude = store[3],
            flyer_url = store[4],
            items = database.get_item_names_by_store_id(id)
        )

# 商品名の一覧を求める
def get_item_names():
    items = database.get_item()
    item_names = []
    for item in items:
        item_names.append(item[1])
    return item_names

# 特売商品情報をリセットする
def clear_item():
    database.clear_item_table()