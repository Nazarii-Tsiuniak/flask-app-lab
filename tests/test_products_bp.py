import unittest
from app import create_app

class ProductsBPTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()
        self.app.testing = True

    def test_products_page(self):
        response = self.app.get('/products/products')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Проєкти', response.data.decode('utf-8'))

    def test_product_detail_page(self):
        response = self.app.get('/products/products/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Портфоліо сайт', response.data.decode('utf-8'))

    def test_product_detail_not_found(self):
        response = self.app.get('/products/products/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Проєкт не знайдено', response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()
