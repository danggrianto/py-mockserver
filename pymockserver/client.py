import requests
import json


class Client(object):

    """Client to connect to the mockserver"""

    def __init__(self, host='localhost', port=1080):
        """
        Class initialization

        :param str host: host of the mockserver
        :param int port: port of the mockserver
        """
        self.host = host
        self.port = port
        self.headers = {
            'Content-Type': 'application/json'
        }

    def _get_url(self):
        """Get full URL of the mockserver

        :return str url of the mockserver
        """
        return 'http://{}:{}'.format(self.host, self.port)

    def expectation(self, request, response):
        """create expectation on mockserver

        :param Request httpRequest object
        :param Response httpResponse object
        """
        data = {
            'httpRequest': request.dict(),
            'httpResponse': response.dict()
        }
        req = requests.put('{}/expectation'.format(self._get_url()),
                           json.dumps(data))
        return req

    def active_expectations(self):
        """Get list of active expectations

        :return Array active expectations
        """
        req = requests.put(
            '{}/retrieve'.format(self._get_url()), params={'type': 'active_expectations'})
        if req.status_code == 200:
            try:
                return req.json()
            except ValueError:
                return []
        return []

    def retrieve_requests(self):
        """Get all recorded requests

        :return Array recorded requests
        """
        req = requests.put('{}/retrieve'.format(self._get_url()),
                           params={'type': 'requests'})
        if req.status_code == 200:
            try:
                return req.json()
            except ValueError:
                return []
        return []

    def verify(self, request, times=None):
        """Verify if a request has been received in specific number of times

        :param Request request: Request object to verify
        :param Times times: Times object for count. Default=None, count=1
        :return Boolean true if verified, false if not
        """
        data = {
            'httpRequest': request.dict()
        }
        if times:
            data['times'] = times.dict()
        else:
            data['times'] = {
                'count': 1,
                'exact': True
            }
        req = requests.put('{}/verify'.format(self._get_url()),
                           headers=self.headers,
                           data=json.dumps(data))
        resp = {
            'status': 'ERROR',
            'reason': req.content.decode('utf-8')
        }
        if req.status_code == 202:
            resp['reason'] = None
            resp['status'] = 'FOUND'
        elif req.status_code == 406:
            resp['status'] = 'NOT_FOUND'

        return resp
