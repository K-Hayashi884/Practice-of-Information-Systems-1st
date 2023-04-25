import database_test as database
class storeRequest:
    id: int
    def __init__(self,id):
        self.id = id

class storeResponse:
    test: int
    def __init__(self, test):
        self.test = test

class itemRequest:
    id: int
    def __init__(self,id):
        self.id = id

class itemResponse:
    test: int
    def __init__(self, test):
        self.test = test

def searchByStore(request: storeRequest) -> storeResponse:
    result = database.searchByStore()
    return storeResponse(
        test = request.id
    )

def searchByItem(request: itemRequest) -> itemResponse:
    return itemResponse(
        test = request.id
    )