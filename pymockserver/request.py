import json


class Request(object):

    """"
    httpRequest object for mockserver
    """
    path = ''
    method = ''
    keepAlive = None

    def __init__(self, path, method, keepAlive=None):
        """Initializing httpRequest object

        :param str path: path endpoint
        :param str method: http method to use ('GET', 'POST', 'PUT' etc.)
        """
        self.path = path
        self.method = method
        self.keepAlive = keepAlive

    def dict(self):
        """return dictionary of the request object

        :return dict of httpRequest object
        """
        dct = {
            'path': self.path,
            'method': self.method.upper()
        }
        if self.keepAlive:
            dct['keepAlive'] = self.keepAlive
        return dct

    def json(self):
        """get json format of this object

        :return json object
        """
        return json.dumps(self.dict())
