from flask import request, jsonify
import usecase_test as usecase

class storeRequest:
    store_id: int
    def __init__(self,id):
        store_id = id

class storeRespond:
    test: int
    def __init__(self, t):
        test = t
    def json(self):
        return jsonify({
            "test" : self.test,
        })

class itemRequest:
    item_id: int
    def __init__(id):
        item_id = id
        
class itemRespond:
    test: int
    def __init__(self, t):
        test = t
    def json(self):
        return jsonify({
            "test" : self.test,
        })
    
def searchByStore(request):
    store_id = request.args.get("id", type=int)
    req = storeRequest(
        store_id = store_id
    )
    res = usecase.searchByStore(req)
    return jsonify({"store_id": store_id})

def searchByItem(request):
    item_id = request.args.get("id", type=int)
    req = itemRequest(
        item_id = item_id
    )
    res = usecase.searchByItem(req)
    return jsonify({"item_id": item_id})
