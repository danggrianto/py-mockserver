from pymockserver import VerificationTimes, RequestTimes
from unittest import TestCase


class RequestTimesTest(TestCase):

    def test_init_default(self):
        times = RequestTimes()
        self.assertEqual(1, times.remainingTimes)
        self.assertTrue(times.unlimited)

    def test_init_with_value(self):
        times = RequestTimes(remainingTimes=2, unlimited=False)
        self.assertEqual(2, times.remainingTimes)
        self.assertFalse(times.unlimited)


class VerificationTimesTest(TestCase):

    def test_init_default(self):
        times = VerificationTimes()
        self.assertEqual(1, times.atLeast)
        self.assertEqual(1, times.atMost)

    def test_init_with_value(self):
        times = VerificationTimes(count=2, exact=False)
        self.assertEqual(2, times.atLeast)
        self.assertFalse(hasattr(times, "atMost"))
