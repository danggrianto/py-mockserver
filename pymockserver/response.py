import json


class Response(object):

    """httpResponse for mockserver"""
    status_code = 0
    body = ''

    def __init__(self, status_code, body=''):
        """initialize httpResponse body

        :param int status_code: status code for http response
        :param str body: body of the response
        """
        self.status_code = status_code
        self.body = body

    def dict(self):
        """returning dictionary of response object"""
        return {
            'statusCode': self.status_code,
            'body': self.body
        }

    def json(self):
        """get JSON object of this object

        :return JSON
        """
        return json.dumps(self.dict())
