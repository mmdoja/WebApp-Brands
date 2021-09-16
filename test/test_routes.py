from webappbackend import app
import unittest

class FlaskTestCase(unittest.TestCase):

    #check for response 200 fror each endpoint

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home(self):
        tester = app.test_client(self)
        response = tester.get('/home')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        tester = app.test_client(self)
        response = tester.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        tester = app.test_client(self)
        response = tester.get('/register')
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        tester = app.test_client(self)
        response = tester.get('/about')
        self.assertEqual(response.status_code, 200)

    def test_reset_password(self):
        tester = app.test_client(self)
        response = tester.get('/reset_password')
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
