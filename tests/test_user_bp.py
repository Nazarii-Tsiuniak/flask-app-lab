# tests/test_user_views.py
import unittest
from app import create_app

class UsersViewsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

    def test_login_page(self):
        response = self.client.get('/users/login')
        self.assertEqual(response.status_code, 200)

    def test_profile_redirect_if_not_logged_in(self):
        response = self.client.get('/users/profile', follow_redirects=True)
        self.assertIn("Спершу увійдіть у систему".encode('utf-8'), response.data)

    def test_login_success(self):
        response = self.client.post('/users/login', data={'username':'admin','password':'12345'}, follow_redirects=True)
        self.assertIn("Вхід успішний!".encode('utf-8'), response.data)
        self.assertIn("Профіль".encode('utf-8'), response.data)

    def test_logout(self):
        self.client.post('/users/login', data={'username':'admin','password':'12345'})
        response = self.client.get('/users/logout', follow_redirects=True)
        self.assertIn("Ви вийшли з системи".encode('utf-8'), response.data)
