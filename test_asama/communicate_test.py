from flask import request, jsonify
import usecase_test as usecase

# Jsonへの変換のために, オブジェクトを辞書/リスト/プリミティブ型のみに変換する
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

# オブジェクトをJsonに変換する
def toJson(obj):
    return jsonify(convertObjectToDict(obj))

# 緯度経度, 希望時間を受け取り適切なレシピを返す
def get_recipe(request):
    latitude = request.args.get("latitude", type=float)
    longitude = request.args.get("longitude", type=float)
    time = request.args.get("time", type=int)
    req = usecase.RecipeRequest(
        latitude = latitude,
        longitude = longitude,
        time = time
    )
    res = usecase.get_recipe(req)
    res = toJson(res)
    return res