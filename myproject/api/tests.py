from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
import json

class ApiTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('process')

    def test_valid_request(self):
        data = {
            "batchid": "id0101",
            "payload": [[1, 2], [3, 4]]
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['batchid'], "id0101")
        self.assertEqual(response_data['response'], [3, 7])
        self.assertEqual(response_data['status'], "complete")

    def test_invalid_request(self):
        data = {
            "batchid": "id0101",
            "payload": [[1, 2], [3, "four"]]
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertIn('error', response_data)
