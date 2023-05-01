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

def add_item_by_name(handlings:list[tuple[str, str, int]]):
    store_name_to_id = get_dict_store_name_to_id()
    item_name_to_id = get_dict_item_name_to_id()

    for handling in handlings:
        store_id = store_name_to_id.get(handling[0], -1)
        item_id = item_name_to_id.get(handling[1], -1)
        if store_id < 0:
            continue
        if item_id < 0:
            item_id = database.add_item(handling[1])
            item_name_to_id[handling[1]] = item_id
        database.add_handling(store_id, item_id)

def clear_item():
    database.clear_item()