from flask import request, jsonify
import usecase_test as usecase

def convertObjectToDict(obj):
    if type(obj) is list:
        for i,value in enumerate(obj):
            obj[i] = convertObjectToDict(value)
    elif type(obj) is dict:
        for key, value in obj.items():
            obj[key] = convertObjectToDict(value)
    elif type(obj) in (int, float, str, bool):
        return obj
    else:
        return convertObjectToDict(obj.__dict__)
    return obj

def toJson(obj):
    return jsonify(convertObjectToDict(obj))

def searchByStore(request):
    store_id = request.args.get("id", type=int)
    req = usecase.storeRequest(
        id = store_id
    )
    res = usecase.searchByStore(req)
    res = toJson(res)
    return res

def searchByItem(request):
    item_id = request.args.get("id", type=int)
    req = usecase.itemRequest(
        id = item_id
    )
    res = usecase.searchByItem(req)
    res = toJson(res)
    return res