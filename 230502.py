from local_settings import SUBSCRIPTION_KEY

import requests
import csv
import http.client, urllib.request, urllib.parse
import urllib.error, base64
import ast
import time
import json
import urllib.parse

def ocr(url,storename):
    # 画像のURLを指定する

    # 画像をダウンロードする
    response = requests.get(url)

    # 画像を保存する
    with open("image.jpg", "wb") as f:
        f.write(response.content)


    # OCR対象のファイル名を定義します
    FILE_NAME = "image.jpg"

    # Computer Visionリソースのサブスクリプションキー、エンドポイント設定
    # サブスクリプションキーとエンドポイントは、リソースグループ作成時に控えておいたキー1,エンドポイントを入力します。
    ENDPOINT ="https://2023-practice-group6.cognitiveservices.azure.com/"

    # ホストを設定
    host = ENDPOINT.split("/")[2]

    # vision-v3.2のread機能のURLを設定
    text_recognition_url = (ENDPOINT + "vision/v3.2/read/analyze")

    # 読み取り用のヘッダー作成
    read_headers = {
        # サブスクリプションキーの設定
        "Ocp-Apim-Subscription-Key":SUBSCRIPTION_KEY,
        # bodyの形式を指定、json=URL/octet-stream=バイナリデータ
        "Content-Type":"application/octet-stream"
    }

    # 結果取得用のヘッダー作成
    result_headers = {
        # サブスクリプションキーの設定
        "Ocp-Apim-Subscription-Key":SUBSCRIPTION_KEY,
    }



    # Read APIを呼ぶ関数
    def call_read_api(host, text_recognition_url, body, params, read_headers):
        # Read APIの呼び出し
        try:
            conn = http.client.HTTPSConnection(host)
            # 読み取りリクエスト
            conn.request(
                method = "POST",
                url = text_recognition_url + "?%s" % params,
                body = body,
                headers = read_headers,
            )

            # 読み取りレスポンス
            read_response = conn.getresponse()
            print(read_response.status)

            # レスポンスの中から読み取りのOperation-Location URLを取得
            OL_url = read_response.headers["Operation-Location"]

            conn.close()
            print("read_request:SUCCESS")

        except Exception as e:
            print("[ErrNo {0}]{1}".format(e.errno,e.strerror))

        return OL_url

    # OCR結果を取得する関数
    def call_get_read_result_api(host, file_name, OL_url, result_headers):
        result_dict = {}
        # Read結果取得
        try:
            conn = http.client.HTTPSConnection(host)

            # 読み取り完了/失敗時にFalseになるフラグ
            poll = True
            while(poll):
                if (OL_url == None):
                    print(file_name + ":None Operation-Location")
                    break

                # 読み取り結果取得
                conn.request(
                    method = "GET",
                    url = OL_url,
                    headers = result_headers,
                )
                result_response = conn.getresponse()
                result_str = result_response.read().decode()
                result_dict = ast.literal_eval(result_str)

                if ("analyzeResult" in result_dict):
                    poll = False
                    print("get_result:SUCCESS")
                elif ("status" in result_dict and 
                    result_dict["status"] == "failed"):
                    poll = False
                    print("get_result:FAILD")
                else:
                    time.sleep(10)
            conn.close()

        except Exception as e:
            print("[ErrNo {0}] {1}".format(e.errno,e.strerror))

        return result_dict



    # body作成
    body = open(FILE_NAME,"rb").read()

    # パラメータの指定
    # 自然な読み取り順序で出力できるオプションを追加
    params = urllib.parse.urlencode({
        # Request parameters
        'readingOrder': 'natural',
    })

    # readAPIを呼んでOperation Location URLを取得
    OL_url = call_read_api(host, text_recognition_url, body, params, read_headers)

    print(OL_url)

    # 処理待ち10秒
    time.sleep(10)

    # Read結果取得
    result_dict = call_get_read_result_api(host, FILE_NAME, OL_url, result_headers)

    # 文字列だけを引く
    def get_str(arg):
        res =[]
        if isinstance(arg, list):
            for item in arg:
                res += get_str(item)
        elif isinstance(arg, dict):
            for key, value in arg.items():
                if key == "text":
                    res.append(value)
                else: 
                    res += get_str(value)
        return res

    str_list = get_str(result_dict) # ["x", "y", "z"]
    #リストの加工




    # 単語のリストを取得する
    with open('shokuhin.csv', 'r') as f:
        reader = csv.reader(f)
        words = [row[0] for row in reader]
    new_str_list = []

    # str_listの各要素について、以下の処理を繰り返す
    for s in str_list:
        # sがwordsに含まれる単語と部分的に一致しているかどうかを判定する
        if any(word in s for word in words):
            # sに「円」「店」が含まれる場合はスキップする
            if "円" in s or "店" in s:
                continue
            # 「()」と「（）」を排除する
            s = s.replace("()", "").replace("（）", "")
            new_str_list.append(s)


    new_str_list = list(set(new_str_list))

    print(new_str_list)  # 条件に合致した文字列のリストを出力する

 



    #[1,2,3,4]
    #d = {'text':'asama', 'age':22, 'aiueo':[{},{},{}]}
    #d['name']