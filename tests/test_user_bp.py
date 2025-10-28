import unittest
from app import create_app

class UserBPTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app().test_client()
        self.app.testing = True

    def test_login_page(self):
        response = self.app.get('/users/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Login', response.data.decode('utf-8'))

    def test_profile_requires_login(self):
        # Слідуємо за редиректом на login
        response = self.app.get('/users/profile', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Login', response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()
