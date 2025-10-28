# tests/test_products_views.py
import unittest
from app import create_app

class ProductsViewsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

    def test_products_list_page(self):
        response = self.client.get('/products')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Портфоліо сайт".encode('utf-8'), response.data)

    def test_product_detail_page(self):
        response = self.client.get('/products/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Сайт для демонстрації моїх робіт".encode('utf-8'), response.data)

    def test_product_detail_not_found(self):
        response = self.client.get('/products/999')
        self.assertEqual(response.status_code, 404)
