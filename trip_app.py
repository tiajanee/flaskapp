import json
from flask import Flask, request, make_response
from flask_restful import Resource, Api
from pymongo import ReturnDocument
import pdb
# 1
from pymongo import MongoClient
# For serialization
from bson import Binary, Code
from bson.json_util import dumps

from encoder import JSONEncoder
app = Flask(__name__)
api = Api(app)

# 2
mongo = MongoClient('localhost', 27017)

# 3
app.db = mongo.local


class User(Resource):
    #functioning
    def post(self):

        name = request.args.get('name')

        new_user = request.json

        users_collection = app.db.users

        result = users_collection.insert_one(new_user)

        user = users_collection.find_one({'name': name})

        #json_result = JSONEncoder().encode(result)

        return (new_user, 200, None)
    #functioning
    def get(self):

        # 1 Get Url params
        name = request.args.get('name')

        # 2 Our users users collection
        users_collection = app.db.users

        # 3 Find document in users collection
        result = users_collection.find_one(
            {'name': name}
        )

        # 4 Convert result to json from python dict
        #json_result = JSONEncoder().encode(result)

        # 5 Return json as part of the response body
        return (result, 200, None)

    def put(self):

        name = request.args.get('name')

        users_collection = app.db.users

        # 2 parsed Request Body
        new_user = request.json

        result = users_collection.find_one_and_replace(
            {'name': name}, 
            new_user, 
            return_document=ReturnDocument.AFTER)

        # pdb.set_trace()

        return(new_user, 200, {"Content-Type": "application/json", "User": "Tony TJ"})

    def patch(self):

        name = request.args.get('user')

        users_collection = app.db.users

        # 2 parsed Request Body
        new_user = request.json

        result = users_collection.find_one_and_update(
            {'name': new_user},
            {
                '$set': {'user': new_user["name"], 'age': new_user["age"]}
            },
            return_document=ReturnDocument.AFTER
        )

        return(new_user, 200, {"Content-Type": "application/json", "User": "Tony TJ"})


class Trip(Resource):

    def get(self):
        destination = request.args.get('destination')

        trips_collection = app.db.trips

        result = trips_collection.find_one({'destination': destination})

        return (result, 200, None)

    #functioning
    def post(self):

        trips_collection = app.db.trips

        # 2 parsed Request Body
        new_destination = request.json

        result = trips_collection.insert_one(new_destination)

        trip = trips_collection.find_one({'_id': result.inserted_id})

        # pdb.set_trace()

        return(new_destination, 200, {"Content-Type": "application/json", "User": "Tony TJ"})

    def put(self):

        destination = request.args.get('destination')

        trips_collection = app.db.trips

        # 2 parsed Request Body
        new_destination = request.json

        result = trips_collection.find_one_and_replace({'destination': destination}, new_destination, return_document=ReturnDocument.AFTER)

        # pdb.set_trace()

        return(result, 200, {"Content-Type": "application/json", "User": "Tony TJ"})

    def patch(self):

        destination = request.args.get('destination')

        trips_collection = app.db.trips

        # 2 parsed Request Body
        new_destination = request.json

        result = trips_collection.find_one_and_update(
            {'destination': destination},
            {
                '$set': {'destination': new_destination["destination"], 'trip_day_amount': new_destination["trip_day_amount"]}
            },
            return_document=ReturnDocument.AFTER
        )

        return(result, 200, {"Content-Type": "application/json", "User": "Tony TJ"})


api.add_resource(User, '/users')

api.add_resource(Trip, '/trips')


@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(JSONEncoder().encode(data), code)
    resp.headers.extend(headers or {})
    return resp


if __name__ == '__main__':
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.run(debug=True)