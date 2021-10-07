import unittest

from flask_login import current_user

from base import BaseTestCase

class FlaskTestCase(BaseTestCase):

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home(self):
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)

    def test_reset_password(self):
        response = self.client.get('/reset_password')
        self.assertEqual(response.status_code, 200)

    '''
    def test_jobs_route_requires_login(self):
        response = self.client.get('/jobs', follow_redirects=True)
        self.assertIn(b'Please log in to access this page', response.data)

    def test_account_route_requires_login(self):
        response = self.client.get('/account', follow_redirects=True)
        self.assertIn(b'Please log in to access this page', response.data)

    def test_query_form_route_requires_login(self):
        response = self.client.get('/query', follow_redirects=True)
        self.assertIn(b'Please log in to access this page', response.data)

    def test_add_brand_route_requires_login(self):
        response = self.client.get('/add_brand', follow_redirects=True)
        self.assertFalse(b'Please log in to access this page', response.data)

    def test_logout_route_requires_login(self):
        response = self.client.get('/logout', follow_redirects=True, fetch_redirect_response=False)
        self.assertRedirects(response, '/login?next=%2Flogout')
'''
    def test_incorrect_user_registeration(self):
        with self.client:
            response = self.client.post('/register', data=dict(
                username='Munir', email='somewrongemailaddress',
                password='munir', confirm_password='notsamepassword'
            ), follow_redirects=True)
            self.assertIn(b'Invalid email address.', response.data)
            self.assertIn(b'Field must be equal to password.', response.data)

    # Ensure login behaves correctly with correct credentials
    def test_correct_login(self):
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(email="munir@amazingbrands.group", password="munir"),
                follow_redirects=True
            )
            self.assertTrue(current_user.is_active)

    def test_incorrect_login(self):
        response = self.client.post(
            '/login',
            data=dict(email="wrong", password="wrong"),
            follow_redirects=True
        )
        self.assertIn(b'Invalid email address.', response.data)

    # Ensure logout behaves correctly
    def test_logout(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="munir@amazingbrands.group", password="munir"),
                follow_redirects=True
            )
            response = self.client.get('/logout', follow_redirects=True)
            self.assertFalse(current_user.is_active)

if __name__ == "__main__":
    unittest.main()
