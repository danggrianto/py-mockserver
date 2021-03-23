class RequestTimes(object):
    """Times object for request
    """

    def __init__(self, remainingTimes=1, unlimited=True):
        """
        Request Time initialization
        :param int remainingTimes: Remaining times for request to expire
        :param boolean unlimited: Unlimited times for request, overwrite
        remainingTimes
        """
        self.remainingTimes = remainingTimes
        self.unlimited = unlimited


class VerificationTimes(object):
    """Times object for verification
    """

    def __init__(self, count=1, exact=True):
        self.atLeast = count
        if exact:
            self.atMost = count
