from unittest import TestCase
import requests

from pymockserver import Client, Request, Response
from pymockserver import RequestTimes, VerificationTimes


class IntegrationTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = Client('localhost', 1080)
        cls.request = Request(path='/hello', method='GET')
        cls.response = Response(status_code=200, body='world')
        cls.mock_url = 'http://localhost:1080'

    def tearDown(self):
        self.client.reset()

    def test_expectation(self):
        self.client.expectation(self.request, self.response)
        resp = requests.get('{}/hello'.format(self.mock_url))
        self.assertEqual(200, resp.status_code)
        self.assertEqual(b'world', resp.content)

    def test_no_path(self):
        resp = requests.get('{}/foo'.format(self.mock_url))
        self.assertEqual(404, resp.status_code)

    def test_expectation_with_time(self):
        times = RequestTimes(remainingTimes=1, unlimited=False)
        self.client.expectation(self.request, self.response, times)
        resp = requests.get('{}/hello'.format(self.mock_url))
        self.assertEqual(200, resp.status_code)
        resp = requests.get('{}/hello'.format(self.mock_url))
        self.assertEqual(404, resp.status_code)

    def test_verification(self):
        self.client.expectation(self.request, self.response)
        requests.get('{}/hello'.format(self.mock_url))
        verified = self.client.verify(self.request)
        self.assertEqual('OK', verified['status'])
        self.assertTrue(verified['found'])

    def test_verification_with_times(self):
        self.client.expectation(self.request, self.response)
        requests.get('{}/hello'.format(self.mock_url))
        times = VerificationTimes(count=2, exact=True)
        verified = self.client.verify(self.request, times)
        self.assertEqual('OK', verified['status'])
        self.assertFalse(verified['found'])

    def test_clear(self):
        self.client.expectation(self.request, self.response)
        new_req = Request('/world', 'GET')
        self.client.expectation(new_req, self.response)
        resp_hello = requests.get('{}/hello'.format(self.mock_url))
        resp_world = requests.get('{}/world'.format(self.mock_url))
        self.assertEqual(200, resp_hello.status_code)
        self.assertEqual(200, resp_world.status_code)
        # delete /hello endpoint
        self.client.clear(self.request)
        verified = self.client.verify(self.request)
        self.assertFalse(verified['found'])

        # should not delete the other end point
        verified = self.client.verify(new_req)
        self.assertTrue(verified['found'])

    def test_reset(self):
        self.client.expectation(self.request, self.response)
        new_req = Request('/world', 'GET')
        self.client.expectation(new_req, self.response)
        resp_hello = requests.get('{}/hello'.format(self.mock_url))
        resp_world = requests.get('{}/world'.format(self.mock_url))
        self.assertEqual(200, resp_hello.status_code)
        self.assertEqual(200, resp_world.status_code)
        # delete all  endpoint
        self.client.reset()
        verified = self.client.verify(self.request)
        self.assertFalse(verified['found'])
        verified = self.client.verify(new_req)
        self.assertFalse(verified['found'])
