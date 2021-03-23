import requests
import json
from urllib.parse import urljoin


class Client(object):

    """Client to connect to the mockserver"""

    def __init__(self, host='localhost', port=1080, scheme='http', verify_ca=False):
        """
        Class initialization

        :param str host: host of the mockserver
        :param int port: port of the mockserver
        :param str scheme: the scheme to use to connect to the mockserver('http', 'https')
        :param boolean/str verify_ca: (only valid for scheme 'https') if True or a path to a ca certificate the ssl
                                      certificate of the mock server will be verified
        """
        self.host = host
        self.port = port
        self.scheme = scheme
        self.verify_ca = verify_ca
        self.headers = {
            'Content-Type': 'application/json'
        }

    def _get_url(self):
        """Get full URL of the mockserver

        :return str url of the mockserver
        """
        return '{}://{}:{}'.format(self.scheme, self.host, self.port)

    def _put(self, path, *args, **kwargs):
        if self.scheme == 'https':
            kwargs['verify'] = self.verify_ca
        return requests.put(urljoin(self._get_url(), path), *args, **kwargs)

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
        req = self._put('/expectation',
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
        req = self._put('/expectation',
                        json.dumps(data))
        return req

    def active_expectations(self):
        """Get list of active expectations

        :return Array active expectations
        """
        req = self._put('/retrieve', params={'type': 'active_expectations'})
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
        req = self._put('/retrieve',
                        params={'type': 'requests'},
                        data=json.dumps(data))
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
                'count': 1,
                'exact': True
            }
        req = self._put('/verify',
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
        self._put('/reset')

    def clear(self, request):
        """Delete active expectation and recorded request

        :param Request request: Request to clear
        """
        self._put('/clear', data=request.json())
