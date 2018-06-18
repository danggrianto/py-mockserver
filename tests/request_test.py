from pymockserver.request import Request

import json
from unittest import TestCase


class RequestTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.request = Request('/somepath', 'POST')

    def test_init(self):
        self.assertEqual('/somepath', self.request.path)
        self.assertEqual('POST', self.request.method)
        self.assertEqual(False, self.request.keepAlive)

    def test_dict(self):
        self.assertEqual({
            'path': self.request.path,
            'method': self.request.method,
            'keepAlive': self.request.keepAlive
        }, self.request.dict())

    def test_json(self):
        self.assertEqual(json.dumps(self.request.dict()), self.request.json())
