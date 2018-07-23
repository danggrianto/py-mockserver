from pymockserver.forward import Forward

import json
from unittest import TestCase


class ForwardTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.forward = Forward('1.2.3.4', 123)

    def test_init(self):
        self.assertEqual('1.2.3.4', self.forward.host)
        self.assertEqual(123, self.forward.port)
        self.assertEqual('HTTP', self.forward.scheme)

    def test_dict(self):
        self.assertDictEqual({
            'host': self.forward.host,
            'port': self.forward.port,
            'scheme': self.forward.scheme
        }, self.forward.dict())

    def test_json(self):
        self.assertEqual(json.dumps(self.forward.dict()),
                         self.forward.json())
