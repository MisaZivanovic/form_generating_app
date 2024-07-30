import unittest
from form_app import app

class FormAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Submit Your Information', response.data)

    def test_submit_success(self):
        response = self.app.post('/submit', data={
            'name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'phone': '1234567890',
            'city': 'Test City'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertEqual(response.location, 'http://localhost/')  # Redirect location should be the index page

    def test_submit_failure(self):
        response = self.app.post('/submit', data={
            'name': '',
            'last_name': '',
            'email': 'invalidemail',
            'phone': '123',
            'city': ''
        })
        self.assertNotEqual(response.status_code, 200)  # Should not be a successful request

if __name__ == '__main__':
    unittest.main()
