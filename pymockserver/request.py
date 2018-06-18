import json


class Request(object):

    """"
    httpRequest object for mockserver
    """
    path = ''
    method = ''
    keepAlive = False

    def __init__(self, path, method):
        """Initializing httpRequest object

        :param str path: path endpoint
        :param str method: http method to use ('GET', 'POST', 'PUT' etc.)
        """
        self.path = path
        self.method = method

    def dict(self):
        """return dictionary of the request object

        :return dict of httpRequest object
        """
        return {
            'path': self.path,
            'method': self.method.upper(),
            'keepAlive': self.keepAlive
        }

    def json(self):
        """get json format of this object

        :return json object
        """
        return json.dumps(self.dict())
