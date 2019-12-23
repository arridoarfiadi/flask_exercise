from flask import Flask, request
from flask_restful import Resource, Api,reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity


app = Flask(__name__)
app.secret_key = 'tiger'
api = Api(app)

jwt = JWT(app, authenticate, identity) #/auth resource is created

items = []

#every resource has to be a class
class Item(Resource):
    #parses the request with only the specified arguments, everything else will be disregarded
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be blank!"
    )
    @jwt_required()
    def get(self,name):
        default_return = {'message': 'item not found'} , 404
        item = next(filter(lambda x: x['name'] == name, items), None)
        return default_return if item is None else item
        
    def post(self,name): #uses url name instead of using it from the payload
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': 'item already exist'}, 400

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201 #created HTTP status code
    def put(self,name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            return {'message':'item does not exist'},404
        else:
            item.update(data) #name in the request will be not be used since we added the parser
        return item
    def delete(self,name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'item deleted'},200

class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(ItemList,'/items')
api.add_resource(Item, '/item/<string:name>')

app.run(port=5000, debug=True)