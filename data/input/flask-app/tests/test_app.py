import unittest
from app import app

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    # Test for addition route
    def test_add(self):
        response = self.app.get('/add?a=5&b=3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['result'], 8)

    def test_add_invalid_input(self):
        response = self.app.get('/add?a=5&b=abc')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

    # Test for subtraction route
    def test_subtract(self):
        response = self.app.get('/subtract?a=10&b=4')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['result'], 6)

    # Test for multiplication route
    def test_multiply(self):
        response = self.app.get('/multiply?a=7&b=6')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['result'], 42)

    # Test for division route
    def test_divide(self):
        response = self.app.get('/divide?a=20&b=4')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['result'], 5.0)

    def test_divide_by_zero(self):
        response = self.app.get('/divide?a=20&b=0')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

    # Test for health check route
    def test_health_check(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'healthy')

if __name__ == '__main__':
    unittest.main()
