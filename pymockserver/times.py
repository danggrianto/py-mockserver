class RequestTimes(object):
    """Times object for request
    """

    def __init__(self, remaining=1, unlimited=True):
        """
        Request Time initialization
        :param int remaining: Remaining times for request to expire
        :param boolean unlimited: Unlimited times for request, overwrite
        remaining
        """
        self.remaining = remaining
        self.unlimited = unlimited


class VerificationTimes(object):
    """Times object for verification
    """

    def __init__(self, count=1, exact=True):
        self.count = count
        self.exact = exact
