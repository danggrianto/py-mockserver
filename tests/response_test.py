from pymockserver.response import Response

import json
from unittest import TestCase


class ResponseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.response = Response(200, 'body')

    def test_init(self):
        self.assertEqual(200, self.response.status_code)
        self.assertEqual('body', self.response.body)

    def test_dict(self):
        self.assertEqual({
            'statusCode': self.response.status_code,
            'body': self.response.body
        }, self.response.dict())

    def test_json(self):
        self.assertEqual(json.dumps(self.response.dict()),
                         self.response.json())
