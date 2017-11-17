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

    def test_getting_a_user(self):

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


if __name__ == '__main__':
    unittest.main()