from flask import jsonify
import test_asama.usecase_test as usecase

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
    latitude = request.args.get("latitude", -1.0)
    longitude = request.args.get("longitude", -1.0)
    time = request.args.get("time", 1000)
    req = usecase.RecipeRequest(
        latitude = latitude,
        longitude = longitude,
        time = time
    )
    res = usecase.get_recipe(req)
    res = toJson(res)
    return res

# 登録されている店名の一覧を求める
def get_store_names(request):
    latitude = float(request.args.get("latitude", -1.0))
    longitude = float(request.args.get("longitude", -1.0))
    length = float(request.args.get("length", 100000.0))
    req = usecase.StoreInfoRequest(
        latitude=latitude,
        longitude=longitude,
        length=length
    )
    res = usecase.get_store_names(req)
    res = toJson(res)
    return res

# 指定した範囲内の店の情報と扱っている特売商品名を求める
def get_store_info(request):
    latitude = float(request.args.get("latitude", -1.0))
    longitude = float(request.args.get("longitude", -1.0))
    length = float(request.args.get("length", 100000.0))
    req = usecase.StoreInfoRequest(
        latitude=latitude,
        longitude=longitude,
        length=length
    )
    res = usecase.get_store_info(req)
    res = toJson(res)
    return res

# 名前で指定した店の情報と扱っている特売商品名を求める
def get_store_info(request):
    name = float(request.args.get("store_name", ""))
    res = usecase.get_store_info(name)
    res = toJson(res)
    return res

# 登録されている特売商品名を求める
def get_item_names(request):
    res = usecase.get_item_names()
    res = toJson(res)
    return res

# 店名から扱っている特売商品名を求める
def get_items_by_store(request):
    name = request.args.get("name", type=str)
    res = usecase.get_items_by_store(name)
    res = toJson(res)
    return res