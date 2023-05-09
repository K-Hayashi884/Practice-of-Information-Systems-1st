from flask import Flask, request
import test_asama.communicate_test as communicate

app = Flask(__name__)

@app.route('/recipe', methods=['GET'])
def get_recipe_request():
    return communicate.get_recipe(request)

@app.route('/store/names', methods=['GET'])
def get_store_names_request():
    return communicate.get_store_names(request)

@app.route('/store/all-info', methods=['GET'])
def get_store_all_info_request():
    return communicate.get_store_info(request)

@app.route('/store/info', methods=['GET'])
def get_store_info_request():
    return communicate.get_store_info_by_name(request)

@app.route('/item', methods=['GET'])
def get_item_names_request():
    return communicate.get_item_names(request)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)