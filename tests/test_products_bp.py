import unittest
from app import create_app

class ProductsBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def test_products_home(self):
        response = self.client.get("/products/")  # обов'язково префікс Blueprint
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Products Home", response.data)  # текст у відповіді

    def test_products_item(self):
        response = self.client.get("/products/1")  # правильно для твого Blueprint
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Product 1", response.data)  # текст у відповіді

if __name__ == "__main__":
    unittest.main()
