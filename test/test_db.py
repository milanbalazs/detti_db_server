import unittest
import sys
import os

sys.path.append(os.path.join(os.path.realpath(os.path.dirname(__file__)), ".."))

from detti_db import DettiDB  # noqa: E402


class DettiDBTestCases(unittest.TestCase):
    """
    This class contains all TestCases for detti DB.
    """

    def __init__(self, *args, **kwargs):
        super(DettiDBTestCases, self).__init__(*args, **kwargs)
        # Show the complete diff in case of error
        self.maxDiff = None
        self.detti_db = DettiDB()

    def test_method(self):
        self.assertTrue(True)
