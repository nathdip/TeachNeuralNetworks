from flask import Flask, request, jsonify
import json
import numpy as np
import pickle
import os

app = Flask(__name__)

file_path = 'data/jsons/'
file_name = 'itemlist.pickle'
if os.path.exists(file_path+file_name):
    with open(file_path+file_name, 'rb') as f:
        itemlist = pickle.load(f)['items']
else:
    itemlist = []


@app.route('/HelloWorld')
def HelloWorld():
    return 'Hello World'


@app.route('/item/<string:name>', methods=['POST'])
def item(name):
    data = request.get_json()
    price = data['price']
    item = {'name': name, 'price': price}
    itemlist.append(item)
    with open(file_path+file_name, 'wb') as f:
        save_list = {'items': itemlist}
        pickle.dump(save_list, f)
    return jsonify(item), 201


@app.route('/item/<string:name>')
def get_item(name):
    item = filter(lambda x: x['name'] == name, itemlist)
    for x in item:
        return jsonify(x), 201
    return jsonify({"Item": None}), 404


@app.route('/items')
def items():
    return jsonify({'items': itemlist}), 201


if __name__ == "__main__":
    app.run()
