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

    	response = self.app.get('/users',
    		query_string=dict(name='TJ King'))

    	response_json = json.loads(response.data.decode())

    	self.assertEqual(response.status_code, 200)

    def test_post_a_user(self):

    ## Post 2 users to database
    	self.app.post('/users',
                      headers=None,
                      data=json.dumps(dict(
                          name="Eliel Gordon",
                          email="eliel@example.com"
                      )),
                      content_type='application/json')
    
    ## 3 Make a get request to fetch the posted user

    	response = self.app.get('/users',
                            query_string=dict(name="Eliel Gordon")
                        )
                                
    # Decode reponse
    	response_json = json.loads(response.data.decode())
    
    ## Actual test to see if GET request was succesful
    ## Here we check the status code
    	self.assertEqual(response.status_code, 200)

    def test_updating_user(self):

    	self.app.post('/users',
    			headers=None,
    			data=json.dumps(dict(
    				name="TJ King",
    				email="tia@email.com"
    				)),
    			content_type='application/json')

    	self.app.put('/users',
    				headers=None,
    				data=json.dumps(dict(
    					name="Tia King")),
    			content_type='application/json')

    	response = self.app.get('/users',
    						query_string=dict(name="Tia King")
    			)

    	response_json = json.loads(response.data.decode())
    	self.assertEqual(response.status_code, 200)

    def test_replace_user(self):
    	self.app.post('/users',
    			headers=None,
    			data=json.dumps(dict(
    				name="TJ King",
    				age=10
    				)),
    			content_type='application/json')

    	self.app.patch('/users',
    			headers=None,
    			data=json.dumps(dict(
    				name="Tia King",
    				age=9)),
    			content_type='application/json')

    	response = self.app.get('/users',
    						query_string=dict(name="Tia King"))

    	response_json = json.loads(response.data.decode())
    	self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
    	self.app.post('/users',
    			headers=None,
    			data=json.dumps(dict(
    				name="TJ King",
    				)),
    			content_type='application/json')

    	response = self.app.delete('/users',
    			headers=None,
    			data=json.dumps(dict(
    				name="TJ King",
    				)),
    			content_type='application/json')
    	# response = self.app.get('users', 
    	# 					query_string=dict(name="TJ King"))
    	
    	response_json = json.loads(response.data.decode())
    	self.assertEqual(response.status_code, 200)

    def test_get_a_trip(self):
    	response = self.app.get('/trips',
    		query_string=dict(destination='Seoul'))

    	response_json = json.loads(response.data.decode())

    	self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()