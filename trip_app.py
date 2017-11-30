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

import bcrypt

from encoder import JSONEncoder
app = Flask(__name__)
api = Api(app)

# 2
mongo = MongoClient('localhost', 27017)

# 3
app.db = mongo.local

app.bcrypt_rounds = 5


class User(Resource):
    def post(self):

        #CREATE A USER

        #getting the data from the body
        new_user = request.json
        users_collection = app.db.users

        #accessing the data and saving them in variables 
        email = new_user["email"]
        password = new_user["password"]

        #check if the user already exists 
        check_saved_user = users_collection.find_one( {"email": email} )

        #if the inputted email already matches a email and the database
        #alert user that the email has been taken 
        if check_saved_user is not None:
            return("This email is taken.", 500, None)

        #if the email doesn't already exists in the database
        #store email and encode and hash password to be saved in database
        if email != check_saved_user:
            encoded_password = password.encode('utf-8')

            hashed = bcrypt.hashpw(
                encoded_password, bcrypt.gensalt(app.bcrypt_rounds)
            )
            new_user["password"] = hashed.decode()
            #insert user and user details to database
            result = users_collection.insert_one(new_user)
            
        return("New user created.", 200, None)

        
    def get(self):

        #LOG IN

        #get users collection from DB
        users_collection = app.db.users

        #get the email and password from the headers
        email = request.authorization.username
        password = request.authorization.password

        #encode the password sent by the attempted user
        encoded_password = password.encode('utf-8')


        #find the user that has that possess that email
        check_saved_user = users_collection.find_one({"email": email})
        #login will fail if user tries to retrieve credentials not in the database
        if check_saved_user is None:
            return("No users with those credientials exist.", 404, None)
        #find the password that matches that user
        check_saved_user_password = check_saved_user["password"]

        #encode the password 
        check_saved_user_password = check_saved_user_password.encode('utf-8')

        #check to see if the encoded inputted password matches encoded password in the database
        if bcrypt.checkpw(encoded_password, check_saved_user_password) == True:
             return("Login Successful", 200, None)
        #accounts for any other edge cases
        else:
            return("Login Unsuccessful", 401, None)
        


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

        return(new_user, 200, {"Content-Type": "application/json", "User": "TJ"})

    def patch(self):

        name = request.args.get('name')

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

        return(new_user, 200, {"Content-Type": "application/json", "User": "TJ"})

    def delete(self):

        name = request.args.get('name')

        users_collection = app.db.users

        result = users_collection.find_one_and_delete({'name': name})

        # import pdb; pdb.set_trace
        if result is None:
            print("wow this bitch is still here")
        
        return("User Deleted", 200, {"Content-Type": "application/json", "User": "TJ"})



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

        return(new_destination, 200, {"Content-Type": "application/json", "User": "TJ"})

    def put(self):

        destination = request.args.get('destination')

        trips_collection = app.db.trips

        # 2 parsed Request Body
        new_destination = request.json

        result = trips_collection.find_one_and_replace({'destination': destination}, new_destination, return_document=ReturnDocument.AFTER)

        # pdb.set_trace()

        return(result, 200, {"Content-Type": "application/json", "User": "TJ"})

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

        return(result, 200, {"Content-Type": "application/json", "User": "TJ"})

    def delete(self):

        destination = request.args.get('destination')

        trips_collection = app.db.trips

        result = trips_collection.find_one_and_delete(
            {'destination': destination}
            )
        return ("Trip Deleted", 200, {"Content-Type": "application/json", "User": "TJ"})


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