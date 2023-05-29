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

class ItemRequest:
    latitude: float
    longitude: float
    length: float
    name: str
    def __init__(self, latitude:float, longitude:float, length:float, name:str):
        self.latitude = latitude
        self.longitude = longitude
        self.length = length
        self.name = name

class StoreRequest:
    latitude: float
    longitude: float
    length: float
    name: str
    def __init__(self, latitude:float, longitude:float, length:float, name:str):
        self.latitude = latitude
        self.longitude = longitude
        self.length = length
        self.name = name

class Store:
    name:str
    latitude:str
    longitude:str
    flyer_url:str
    url_type:int
    items:list[str]
    def __init__(self, name:str, latitude:float, longitude:float, flyer_url:str, url_type:int, items:list[str]):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.flyer_url = flyer_url
        self.url_type = url_type
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
    items = list(set(items))
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

# 特売品のリストの中にどれだけ材料リストの要素が含まれるかを調べる
def calc_simirality(ingredients:list[str], items:list[tuple[str,int]]):
    score = 0
    store_list = []
    for ingredient in ingredients:
        for item in items:
            if ingredient in item[0] or item[0] in ingredient:
                score += 1
                store_list.append((ingredient, item[1]))
    score /= min(10,len(ingredients))
    return score, store_list

# 最適なレシピを求める
def get_recipe(request:RecipeRequest):
    
    # 周辺のスーパーの特売品一覧を生成
    store_info = get_store_info(
        StoreInfoRequest(
        latitude=request.latitude,
        longitude=request.longitude,
        length=request.length
    ))
    items = []
    for i,store in enumerate(store_info):
        for item in store.items:
            items.append((item,i))
    
    # レシピを取得
    recipes = database.get_recipe()
    recipe_info_list = []
    score_and_recipe = []
    store_lists = [[]] * len(recipes)

    # 特売品が多く含まれる順にレシピをソート
    for i,recipe in enumerate(recipes):
        id = recipe[0]
        ingredients = database.get_ingredient_names_by_recipe_id(id)
        print(ingredients)
        score, store_lists[i] = calc_simirality(ingredients, items)
        score_and_recipe.append([score,i])
    #score_and_recipe.sort(reverse=True)

    # 上位数件のレシピデータを出力用に整形
    for recipe in recipes:
        id = recipe[0]
        recipe_info_list.append(Recipe(
                name = recipe[1],
                time = recipe[2],
                url = recipe[3],
                ingredients = database.get_ingredient_names_by_recipe_id(id),
                stores = []
        ))

    # 特売品を販売しているスーパーで分ける
    for i, recipe in enumerate(recipe_info_list):
        store_to_ingredients_dict: dict[int,list[str]] = {}
        store_list = store_lists[score_and_recipe[i][1]]
        for ingredient, store_idx in store_list:
            if store_idx in store_to_ingredients_dict.keys():
                store_to_ingredients_dict[store_idx].append(ingredient)
            else:
                store_to_ingredients_dict[store_idx] = [ingredient]
        for store_idx, ingredient_list in store_to_ingredients_dict.items():
            recipe_info_list[i].stores.append(
                Store(
                    name=store_info[store_idx].name,
                    latitude=store_info[store_idx].latitude,
                    longitude=store_info[store_idx].longitude,
                    flyer_url=store_info[store_idx].flyer_url,
                    url_type=store_info[store_idx].url_type,
                    items=list(set(ingredient_list))
                )
            )

    for i, recipe in enumerate(recipe_info_list):
        if len(recipe.stores) > 0:
            score_and_recipe[i][0] = score_and_recipe[i][0]**(1/len(recipe_info_list[i].stores))
        else:
            score_and_recipe[i][0] = 0

        if recipe.time <= request.time:
            score_and_recipe[i][0] = score_and_recipe[i][0]**(1/(request.time-recipe.time+1))
        else:
            score_and_recipe[i][0] = 0

    score_and_recipe.sort(reverse=True)
    result = []
    for [score, i] in score_and_recipe:
        if score > 0:
            result.append(recipe_info_list[i])
    return result[:min(10,len(result))]

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
            url_type = store[5],
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
            url_type = store[5],
            items = database.get_item_names_by_store_id(id)
        )
    return []

# 商品名の一覧を求める
def get_items_by_name(request):
    item_name = request.name
    stores = get_store_info(StoreInfoRequest(
        latitude=request.latitude,
        longitude=request.longitude,
        length=request.length
    ))
    result = []
    for i, store in enumerate(stores):
        items = []
        for item in store.items:
            if item_name in item or item in item_name:
                items.append(item)
        stores[i].items = items
        if len(items) > 0:
            result.append(stores[i])
    return result

# 店情報の一覧を求める
def get_stores_by_name(request):
    store_name = request.name
    stores = get_store_info(StoreInfoRequest(
        latitude=request.latitude,
        longitude=request.longitude,
        length=request.length
    ))
    result = []
    for i, store in enumerate(stores):
        if store_name in store.name or store.name in store_name:
            result.append(store)
    return result

# 店名とURLを取得する
def get_store_url():
    request = StoreInfoRequest(
        latitude=135,
        longitude=35,
        length=100000
    )
    stores = get_store_info(request)
    store_info = []
    for store in stores:
        store_info.append((store.name, store.flyer_url, store.url_type))
    return store_info

# 特売商品情報をリセットする
def clear_item():
    database.clear_item_table()