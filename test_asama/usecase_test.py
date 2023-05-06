import database_test as database
class storeRequest:
    id: int
    def __init__(self,id):
        self.id = id

class storeResponse:
    store_names: list
    def __init__(self, store_name_list):
        self.store_names = store_name_list

class itemRequest:
    id: int
    def __init__(self,id):
        self.id = id

class itemResponse:
    test: int
    def __init__(self, test):
        self.test = test

def searchByStore(request: storeRequest) -> storeResponse:
    result = database.searchByStore(request.id)
    response = storeResponse(result)
    return response

def searchByItem(request: itemRequest) -> itemResponse:
    return itemResponse(
        test = request.id
    )

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

def clear_item():
    database.clear_item()