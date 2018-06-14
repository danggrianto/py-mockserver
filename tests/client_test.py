from pymockserver.client import Client
from pymockserver.request import Request
from pymockserver.response import Response

import json
from unittest import TestCase
from unittest.mock import Mock, patch


class ClientTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = Client('localhost', 1080)
        cls.base_url = 'http://localhost:1080'

    def test_init(self):
        self.assertEqual('localhost', self.client.host)
        self.assertEqual(1080, self.client.port)

    def test_get_url(self):
        self.assertEqual(self.base_url, self.client._get_url())

    @patch('pymockserver.client.requests.put')
    def test_expectation(self, mocked_put):
        request = Request('/hello', 'POST')
        response = Response(200, 'world')
        response = self.client.expectation(request, response)

        data = {
            'httpRequest': {
                'path': '/hello',
                'method': 'POST',
                'keepAlive': True
            },
            'httpResponse': {
                'statusCode': 200,
                'body': 'world'
            }
        }
        mocked_put.assert_called_with('{}/expectation'.format(self.base_url),
                                      json.dumps(data))

    @patch('pymockserver.client.requests.put')
    def test_active_expectations(self, mocked_put):
        mocked_put.return_value.status_code = 500
        expectations = self.client.active_expectations()
        mocked_put.assert_called_with('{}/retrieve'.format(self.base_url),
                                      params={'type': 'active_expectations'})
        self.assertEqual([], expectations)

    @patch('pymockserver.client.requests.put')
    def test_retrieve_requests(self, mocked):
        mocked.return_value.status_code = 500
        requests = self.client.retrieve_requests()
        mocked.assert_called_with('{}/retrieve'.format(self.base_url),
                                  params={'type': 'requests'})
        self.assertEqual([], requests)
