import json


class Forward(object):

    """httpForward for mockserver"""
    host = '0.0.0.0'
    port = 1080
    scheme = 'HTTP'

    def __init__(self, host, port):
        """initialize httpForward Body

        :param str host: host to mock
        :param int port: port to mock
        """
        self.host = host
        self.port = port

    def dict(self):
        """returning dictionary of response object"""
        return {
            'host': self.host,
            'port': self.port,
            'scheme': self.scheme
        }

    def json(self):
        """get JSON object of this object

        :return JSON
        """
        return json.dumps(self.dict())
