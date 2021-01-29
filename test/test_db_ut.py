import unittest
import sys
import os
import shutil
import json
import warnings
from typing import Optional

sys.path.append(os.path.join(os.path.realpath(os.path.dirname(__file__)), ".."))

from detti_db import DettiDB  # noqa: E402


def mock_value_error(*args, **kwargs):
    raise ValueError("Test exception")


class DettiDBTestCases(unittest.TestCase):
    """
    This class contains all TestCases for detti DB.
    """

    def __init__(self, *args, **kwargs) -> None:
        super(DettiDBTestCases, self).__init__(*args, **kwargs)
        # Show the complete diff in case of error
        self.maxDiff: Optional[int] = None
        # The "set_up_default_logger" is tested with this instance creation.
        self.detti_db: DettiDB = DettiDB()

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

        self.detti_db._clear_db()

    def test_magic_methods(self) -> None:
        """
        Testing the magic methods.
            - __getitem__
            - __setitem__
            - __delitem__
        :return: None
        """

        self.detti_db["test_key"] = "test_val"
        self.assertEqual(self.detti_db["test_key"], "test_val")
        del self.detti_db["test_key"]
        self.assertIsNone(self.detti_db["test_key"])

        # Testing the wrong type (The element should be insert to DB.)
        self.detti_db["test_key"] = 18
        self.assertIsNone(self.detti_db["test_key"])

    def test_load_db_non_exit_db_creation(self) -> None:
        """
        Testing the non-exist DB creation in "load_db" method.
        :return: None
        """

        not_exist_db: str = "does/not/exist/data_base.db"

        original_path_of_db: str = self.detti_db.path_of_db
        self.detti_db.path_of_db = not_exist_db

        # The method should return an empty dist
        self.assertEqual(self.detti_db.load_db(), {})

        # The DB should be created by method
        self.assertTrue(os.path.isfile(not_exist_db))

        # Check the permissions of the created DB file
        status = os.stat(not_exist_db)
        self.assertTrue(0o600, status.st_mode & 0o777)

        # Empty DB should return empty dict
        self.assertEqual(self.detti_db.load_db(), {})

        original_json_load: json.load = json.load
        json.load = mock_value_error
        self.detti_db["test_key"] = "test_val"

        with self.assertRaises(ValueError) as value_error:
            self.detti_db.load_db()
            self.assertTrue("Test exception" in str(value_error))

        self.detti_db.path_of_db = original_path_of_db
        shutil.rmtree("does")
