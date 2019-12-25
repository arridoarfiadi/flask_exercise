import sqlite3
from flask import Flask, request
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
#every resource has to be a class
class Item(Resource):
    #parses the request with only the specified arguments, everything else will be disregarded
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be blank!"
    )

    @classmethod
    def find_by_name(cls,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query,(name,))
        row = result.fetchone()
        connection.commit()
        connection.close()
        if row:
            return {'item' : {'name': row[0], 'price': row[1]}}
        return None
        
    #@jwt_required()
    def get(self,name):
        item = Item.find_by_name(name)
        if item: 
            return item, 200
        else:
            return {'message': 'item not found'} , 404

        
    #@jwt_required()
    def post(self,name): #uses url name instead of using it from the payload
        if Item.find_by_name(name) is not None:
            return {'message': 'item already exist'}, 400
        data = Item.parser.parse_args()
        def insert():
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            
            query = "INSERT INTO items VALUES (?, ?)"
            cursor.execute(query,(name, data['price']))
            connection.commit()
            connection.close()        
        try: 
            insert()
        except:
            return {"message":"an error occured while inserting the item"},500

        return {'item' : {'name': name, 'price': data['price']}}, 201
    #@jwt_required()
    def put(self,name):
        data = Item.parser.parse_args()
        item = Item.find_by_name(name)

        if item is None:
            return {'message':'item does not exist'},404
        else:
            def update():
                connection = sqlite3.connect('data.db')
                cursor = connection.cursor()
                data = Item.parser.parse_args()
                query = "UPDATE items SET price=? WHERE name=?"
                cursor.execute(query,(data['price'],name))
                connection.commit()
                connection.close()
            try:
                update()
            except:
                return {"message":"an error occured while inserting the item"},500
            return {'item' : {'name': name, 'price': data['price']}}, 200

    #@jwt_required()
    def delete(self,name):
        if Item.find_by_name(name) is None:
            return {'message': 'item does not exist'}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query,(name,))
        connection.commit()
        connection.close()
        return {"message": "Item deleted successfully."}, 200

class ItemList(Resource):
    #@jwt_required()
    def get(self):
        items = []
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        for row in cursor.execute(query):
            items.append({'name': row[0], 'price': row[1]})
        connection.commit()
        connection.close()
        return {'items': items}