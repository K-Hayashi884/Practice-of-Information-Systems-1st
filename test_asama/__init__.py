from flask import Flask, request
from communicate_test import *

app = Flask(__name__)

@app.route('/recipe', methods=['GET'])
def searchByStoreRequest():
    return get_recipe(request)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)