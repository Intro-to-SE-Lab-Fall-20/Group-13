from app import app
import unittest

class FlaskTestCase(unittest.TestCase):
    
    # ensure that flask was set up
    
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        assert isUserValid("test@test.com","hello") == (True,3)  
    
    if __name__ == '__main__':
        unittest.main()
        
   #test 