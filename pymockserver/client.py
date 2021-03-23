import requests
import json

from urllib3.exceptions import HTTPError


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

    def expectation(self, request, response, times=None):
        """create expectation on mockserver

        :param request httpRequest object
        :param response httpResponse object
        """
        data = {
            'httpRequest': request.dict(),
            'httpResponse': response.dict(),
            'times': {
                'remainingTimes': 1,
                'unlimited': True
            }
        }
        if times:
            data['times'] = vars(times)
        req = requests.put('{}/expectation'.format(self._get_url()),
                           json.dumps(data))
        return req

    def forward(self, request, forward, times=None):
        """create forwarding on mockserver

        :param times: times object (optional)
        :param request httpRequest object
        :param forward httpResponse object
        """
        data = {
            'httpRequest': request.dict(),
            'httpForward': forward.dict(),
            'times': {
                'remainingTimes': 1,
                'unlimited': True
            }
        }
        if times:
            data['times'] = vars(times)
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

    def retrieve_requests(self, request=None):
        """Get all recorded requests

        :return Array recorded requests
        """
        data = {}
        if request:
            data = request.dict()
        req = requests.put('{}/retrieve'.format(self._get_url()),
                           params={'type': 'requests'}, data=json.dumps(data))
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
            data['times'] = vars(times)
        else:
            data['times'] = {
                'atLeast': 1,
                'atMost': 1
            }
        req = requests.put('{}/verify'.format(self._get_url()),
                           headers=self.headers,
                           data=json.dumps(data))
        resp = {
            'status': 'OK',
            'reason': req.content.decode('utf-8'),
            'found': None
        }
        if req.status_code == 202:
            resp['reason'] = None
            resp['found'] = True
        elif req.status_code == 406:
            resp['found'] = False
        else:
            resp['status'] = 'ERROR'

        return resp

    def reset(self):
        """delete all active expectations and recorded requests"""
        requests.put('{}/reset'.format(self._get_url()))

    def clear(self, request):
        """Delete active expectation and recorded request

        :param Request request: Request to clear
        """
        requests.put('{}/clear'.format(self._get_url()), data=request.json())
