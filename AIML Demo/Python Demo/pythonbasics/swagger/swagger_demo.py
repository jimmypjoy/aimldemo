# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 10:50:26 2024

@author: jimmy
"""

from flask import Flask, request
from flask_restx import Api, Resource, fields

# Initialize Flask app
app = Flask(__name__)

# Initialize Flask-RESTX API
api = Api(app, version='1.0', title='Store API', description='A simple Store API', doc='/swagger')

# Namespace for organization
ns = api.namespace('stores', description='Store operations')

# In-memory data storage
stores = [
    {
        "name": "My Store",
        "items": [
            {"name": "Chair", "price": 15.99},
            {"name": "Table", "price": 30.99}
        ]
    }
]

# Swagger models for input and output
item_model = api.model('Item', {
    'name': fields.String(required=True, description='The name of the item'),
    'price': fields.Float(required=True, description='The price of the item')
})

store_model = api.model('Store', {
    'name': fields.String(required=True, description='The name of the store'),
    'items': fields.List(fields.Nested(item_model))
})

# Routes
@ns.route('/')
class StoreList(Resource):
    @ns.doc('list_stores')
    @ns.marshal_with(store_model, as_list=True)
    def get(self):
        """List all stores"""
        return stores

@ns.route('/<string:name>')
@ns.response(404, 'Store not found')
class Store(Resource):
    @ns.doc('get_store')
    @ns.marshal_with(store_model)
    def get(self, name):
        """Get a store by name"""
        for store in stores:
            if store["name"] == name:
                return store
        api.abort(404, "Store not found")

@ns.route('/<string:name>/item')
@ns.response(404, 'Store not found')
class StoreItems(Resource):
    @ns.doc('get_items_in_store')
    @ns.marshal_with(item_model, as_list=True)
    def get(self, name):
        """Get items in a store by store name"""
        for store in stores:
            if store["name"] == name:
                return store["items"]
        api.abort(404, "Store not found")

@ns.route('/<string:name>/item_create')
@ns.response(404, 'Store not found')
class CreateItem(Resource):
    @ns.doc('create_item')
    @ns.expect(item_model)
    @ns.marshal_with(item_model, code=201)
    def post(self, name):
        """Create a new item in a store"""
        request_data = request.json
        for store in stores:
            if store["name"] == name:
                new_item = {"name": request_data["name"], "price": request_data["price"]}
                store["items"].append(new_item)
                return new_item, 201
        api.abort(404, "Store not found")

# Run the Flask app
if __name__ == "__main__":
    app.run(port=8081, debug=True)
