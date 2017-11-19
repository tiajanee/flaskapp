import trip_app
import unittest
import json
from pymongo import MongoClient

db = None

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.app = trip_app.app.test_client()
        
        # Run app in testing mode to retrieve exceptions and stack traces
        trip_app.app.config['TESTING'] = True
        
        # Inject test database into application
        mongo = MongoClient('localhost', 27017)
        global db
        db = mongo.test_database
        trip_app.app.db = db
        
        ## We do this to clear our database before each test runs
        db.drop_collection('users')


    def test_get_a_user(self):

    	#getting a user
    	response = self.app.get('/users',
    		query_string=dict(name='TJ King'))

    	#decode the response

    	response_json = json.loads(response.data.decode())

    	#Here we check the status code
    	self.assertEqual(response.status_code, 200)

    def test_post_a_user(self):

    # posting user to database
    	self.app.post('/users',
                      headers=None,
                      data=json.dumps(dict(
                          name="Eliel Gordon",
                          email="eliel@example.com"
                      )),
                      content_type='application/json')
    
    # using the get method to test the success of the post method

    	response = self.app.get('/users',
                            query_string=dict(name="Eliel Gordon")
                        )
                                
    # Decode reponse
    	response_json = json.loads(response.data.decode())
    
    # if get is successful, we'll get the correct status code
    # Here we check the status code
    	self.assertEqual(response.status_code, 200)

    def test_updating_user(self):
    	# posting user to database

    	self.app.post('/users',
    			headers=None,
    			data=json.dumps(dict(
    				name="TJ King",
    				email="tia@email.com"
    				)),
    			content_type='application/json')

    	#changing just the name of the user using put method
    	self.app.put('/users',
    				headers=None,
    				data=json.dumps(dict(
    					name="Tia King")),
    			content_type='application/json')
    	#use the get method to query the database using the changed name
    	response = self.app.get('/users',
    						query_string=dict(name="Tia King")
    			)

    	# if get is successful, we'll get the correct status code
    	# Here we check the status code

    	response_json = json.loads(response.data.decode())
    	self.assertEqual(response.status_code, 200)

    def test_replace_user(self):
    	# posting user to database
    	self.app.post('/users',
    			headers=None,
    			data=json.dumps(dict(
    				name="TJ King",
    				age=10
    				)),
    			content_type='application/json')
    	# using the patch method to change all aspects of a user, replacing the inital one
    	self.app.patch('/users',
    			headers=None,
    			data=json.dumps(dict(
    				name="Tia King",
    				age=9)),
    			content_type='application/json')
    	#use the get method to query the database using the changed user details
    	response = self.app.get('/users',
    						query_string=dict(name="Tia King"))

    	# if get is successful, we'll get the correct status code
    	# Here we check the status code
    	response_json = json.loads(response.data.decode())
    	self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
    	#post a user to database
    	self.app.post('/users',
    			headers=None,
    			data=json.dumps(dict(
    				name="TJ King",
    				)),
    			content_type='application/json')
    	#search for that user and delete them using delete method
    	response = self.app.delete('/users',
    			headers=None,
    			data=json.dumps(dict(
    				name="TJ King",
    				)),
    			content_type='application/json')
    	
    	# if delete is successful, we'll get the correct status code
    	# Here we check the status code
    	response_json = json.loads(response.data.decode())
    	self.assertEqual(response.status_code, 200)

    def test_get_a_trip(self):
    	 #getting a trip

    	response = self.app.get('/trips',
    		query_string=dict(destination='Seoul'))

    	# Decode reponse
    	response_json = json.loads(response.data.decode())

    	# if get is successful, we'll get the correct status code
    	# Here we check the status code
    	self.assertEqual(response.status_code, 200)

    def test_post_a_trip(self):

    	#posting a test trip to database
    	self.app.post('/trips',
                      headers=None,
                      data=json.dumps(dict(
                          destination="Seoul",
                          trip_day_amount=5
                      )),
                      content_type='application/json')
    
    	#Make a get request to fetch the posted trip

    	response = self.app.get('/trips',
                            query_string=dict(destination="Seoul")
                        )
                                
    # Decode response
    	response_json = json.loads(response.data.decode())
    
    ## if get is successful, we'll get the correct status code
    ## Here we check the status code
    	self.assertEqual(response.status_code, 200)


    def test_updating_trip(self):

    	#post a test trip to database
    	self.app.post('/trips',
    			headers=None,
    			data=json.dumps(dict(
    				destination="Seoul",
                     trip_day_amount=5
    				)),
    			content_type='application/json')

    	#use the put method to change the name of the trip
    	self.app.put('/trips',
    				headers=None,
    				data=json.dumps(dict(
    					destination="San Francisco",
                          trip_day_amount=5)),
    				content_type='application/json')

    	#use get method to fetch updated trip
    	response = self.app.get('/trips',
    						query_string=dict(destination="San Francisco")
    			)

    	#if get is successful, we'll get the correct status code
    	#Here we check the status code
    	response_json = json.loads(response.data.decode())
    	self.assertEqual(response.status_code, 200)


    def test_replace_a_trip(self):

    	#post test trip to database
		self.app.post('/trips',
    			headers=None,
    			data=json.dumps(dict(
    				destination="Seoul",
                    trip_day_amount=5
    				)),
    			content_type='application/json')
		#use patch method to completely change the trip details
		self.app.patch('/trips',
    			headers=None,
    			data=json.dumps(dict(
    				destination="San Francisco",
    				trip_day_amount=9)),
    			content_type='application/json')
		#use get method to fetch the new trip
		response = self.app.get('/trips',
    						query_string=dict(name="San Francisco"))

		#if get is successful, we'll get the correct status code
		#here we check the status code
		response_json = json.loads(response.data.decode())
		self.assertEqual(response.status_code, 200)

    def test_delete_a_trip(self):

    	#post a test trip to the database
    	self.app.post('/trips',
    			headers=None,
    			data=json.dumps(dict(
    				destination="Seoul",
    				)),
    			content_type='application/json')
    	#use the delete method to remove the posted trip
    	response = self.app.delete('/trips',
    			headers=None,
    			data=json.dumps(dict(
    				destination="Seoul",
    				)),
    			content_type='application/json')
    	#check status code to see if it worked
    	response_json = json.loads(response.data.decode())
    	self.assertEqual(response.status_code, 200)



if __name__ == '__main__':
    unittest.main()