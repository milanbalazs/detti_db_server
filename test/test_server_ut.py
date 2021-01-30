import unittest
import sys
import os
import warnings
import configparser
from typing import Optional

sys.path.append(os.path.join(os.path.realpath(os.path.dirname(__file__)), ".."))


def mock_value_error(*args, **kwargs):
    raise ValueError("ValueError Test exception")


def mock_runtime_error(*args, **kwargs):
    raise RuntimeError("RuntimeError Test exception")


def mock_key_error(*args, **kwargs):
    raise KeyError("KeyError Test exception")


class DettiServerTestCases(unittest.TestCase):
    """
    This class contains all TestCases for detti DB.
    """

    def __init__(self, *args, **kwargs) -> None:
        super(DettiServerTestCases, self).__init__(*args, **kwargs)
        # Show the complete diff in case of error
        self.maxDiff: Optional[int] = None
        self.used_ut_config_file = os.path.join(
            os.path.realpath(os.path.dirname(__file__)), "detti_conf_ut.ini"
        )

    def setUp(self) -> None:
        """
        Running before all methods.
        It is an init method for test methods.
        :return:
        """

        warnings.filterwarnings("ignore", category=ResourceWarning)

    def tearDown(self) -> None:
        """
        Running after all methods.
        It is the cleaner method.
        :return: None
        """

        config: configparser.ConfigParser = configparser.ConfigParser(allow_no_value=True)
        config.read(os.path.join(
            os.path.realpath(os.path.dirname(__file__)), "detti_conf_ut.ini"
        ))
        db_file_path: str = config.get("DETTI_DB", "path_of_db")
        if os.path.isfile(db_file_path):
            os.remove(db_file_path)

    def test_ok(self):
        self.assertTrue(True)
