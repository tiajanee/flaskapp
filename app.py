import json
from flask import Flask, request
import pdb

from pymongo import MongoClient
#from encoder import JSONEncoder
from bson import Binary, Code
from bson.json_util import dumps

mongo = MongoClient('localhost', 27017)

app = Flask(__name__)

app.db = mongo.local
# @app.route('/person')
# def person_route():
#     person = {"name": "Eliel", 'age': 23}
#     json_person = json.dumps(person)
#     return (json_person, 200, None)


@app.route('/person')
def person_route():
    ##cpdb.set_trace()
    person = {"name": "Eliel", 'age': 23}
    json_person = json.dumps(person)
    return (json_person, 200, None)


@app.route('/my_page')
def page_route():
	#pdb.set_trace()
	line_of_text = "This here is a motherfucking line of text"
	return (line_of_text, 200, None)

@app.route('/pets')
def pets_route():
	#pdb.set_trace()
	pets_list = [{"Best Pet": "Turtle"}, {"Second Best Pet" :"Hamster"}, {"Third Best Pet": "Penguin"}]
	json_pets = json.dumps(pets_list)
	return (json_pets, 200, None)

@app.route('/users')
def get_users_route():
    #gets the name of the user

    name = request.args.get('name')

    #debugging
    pdb.set_trace()

    #puts users into a collection
    users_collection = app.db.users

    #mongo returns name of user from collection, returns as dict
    result = users_collection.find_one(
        {'name': name}
    )
    #saves result into serialized json object
    json_result = dumps(result)

    #sends result to postman
    return(json_result, 200, None)

@app.route('/sunsign')
def get_sun_sign():
    sun_sign = request.args.get('sun sign')

    users_collection = app.db.users

    result = users_collection.find_one(
        {'sun sign': sun_sign}
    )
    json_result = json.dumps(result)

    return(json_result, 200, None)

@app.route('/courses', methods=['POST'])
def post_a_course():
    #get reques the json body
    course = request.json

    #getting courses collection
    courses_collection = app.db.courses

   

    
    #insert post into courses collection
    result = courses_collection.insert_one(course)
        #{"course": course["course"]}
       

    # pdb.set_trace()

    #serializes JSON body
    json_post = dumps(course)

    #returns status code and sends posts to database
    return(json_post, 201, None)
    

#homework due monday
    '''
    Handle a get request to "courses" that looks for a course number from the url parameter, returns a 400 error if the course number 
    parameter doesn't exit, and uses the course number to search our database courses collection for a document with the specified 
    course number. Return a 200 and the course if its found.
    '''
@app.route('/courses', methods=['GET'])
def get_a_course_number():

    course_number= request.args.get('course_number', type=int)
    #pdb.set_trace()

    courses_collection = app.db.courses

    #pdb.set_trace()
    result = courses_collection.find_one({"course_number": course_number})
    json_result = json.dumps(result)

    if result is None:
        return("we aint got that course", 400, None)
    else:
        return(json_result, 200, None)

if __name__ == '__main__':
	#mongo = MongoClient('localhost', 27017)
	#app.db = mongo.local
	app.config["DEBUG"] = True
	app.run()
