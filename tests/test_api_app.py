import unittest
from api_app import app

class ApiAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_api_data_success(self):
        response = self.app.post('/api/data', json={
            'name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'phone': '1234567890',
            'city': 'Test City'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Data received and email sent', response.data)

    def test_api_data_failure(self):
        response = self.app.post('/api/data', data={
            'name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'phone': '1234567890',
            'city': 'Test City'
        })  # Not JSON data
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Request must be JSON', response.data)

if __name__ == '__main__':
    unittest.main()
