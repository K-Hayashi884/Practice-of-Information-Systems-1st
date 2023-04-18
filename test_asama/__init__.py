from flask import Flask, request, jsonify
from communicate_test import *

app = Flask(__name__)

@app.route('/store', methods=['GET'])
def searchByStoreRequest():
    return searchByStore(request)

@app.route('/item', methods=['GET'])
def searchByItemRequest():
    return searchByItem(request)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)