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
    raise ValueError("ValueError Test exception")


def mock_runtime_error(*args, **kwargs):
    raise RuntimeError("RuntimeError Test exception")


def mock_key_error(*args, **kwargs):
    raise KeyError("KeyError Test exception")


class DettiDBTestCases(unittest.TestCase):
    """
    This class contains all TestCases for detti DB.
    """

    def __init__(self, *args, **kwargs) -> None:
        super(DettiDBTestCases, self).__init__(*args, **kwargs)
        # Show the complete diff in case of error
        self.maxDiff: Optional[int] = None
        # The "set_up_default_logger" is tested with this instance creation.
        self.detti_db: DettiDB = DettiDB(
            config_file=os.path.join(
                os.path.realpath(os.path.dirname(__file__)), "detti_conf_ut.ini"
            )
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

        self.detti_db._clear_db()
        os.remove(self.detti_db.path_of_db)

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

    def test_load_db(self) -> None:
        """
        Testing the complete "load_db" method.
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

        not_exist_db: str = "does/not/exist/data_base_2.db"
        self.detti_db.path_of_db = not_exist_db
        # The method should return an empty dist
        self.assertEqual(self.detti_db.load_db(), {})

        # Put element to the DB
        self.detti_db["test_key"] = "test_val"

        original_json_load: json.load = json.load
        json.load = mock_value_error

        with self.assertRaises(ValueError) as runtime_error:
            self.detti_db.load_db()
            self.assertTrue("ValueError Test exception" in str(runtime_error))

        json.load = mock_runtime_error

        with self.assertRaises(RuntimeError) as value_error:
            self.detti_db.load_db()
            self.assertTrue("RuntimeError Test exception" in str(value_error))

        json.load = original_json_load
        self.detti_db.path_of_db = original_path_of_db
        shutil.rmtree("does")

    def test_get(self) -> None:
        """
        Testing the get method.
        It is also called from __getitem__ method.
        :return: None
        """

        self.assertIsNone(self.detti_db.get("not_exist"))

    def test_get_all(self) -> None:
        """
        Testing the non-exist DB creation in "load_db" method.
        :return: None
        """

        # Testing the return value of an empty DB.
        self.assertEqual(self.detti_db.get_all(), {})

        # Testing the return value of an NON empty DB.
        self.detti_db["test_var"]: str = "test_val"
        self.assertEqual(self.detti_db.get_all(), {"test_var": "test_val"})

    def test_set(self) -> None:
        """
        Testing the set method.
        It is also called from __setitem__ method.
        :return: None
        """

        # Testing the too long value
        self.assertFalse(self.detti_db.set("test_value", "x" * 101))

        # Testing the too long key
        self.assertFalse(self.detti_db.set("x" * 101, "test_val"))

    def test_delete(self) -> None:
        """
        Testing the delete method.
        It is also called from __delitem__ method.
        :return: None
        """

        # Testing if a key is not in the DB
        self.assertFalse(self.detti_db.delete("not_exist_key"))

    def test_search_keys_in_db(self) -> None:
        """
        Testing the "search_keys_in_db" method.
        :return: None
        """

        self.detti_db["test_key"] = "test_val"
        self.detti_db["prod_key_1"] = "prod_val_1"
        self.detti_db["prod_key_2"] = "prod_val_2"

        self.assertEqual(
            self.detti_db.search_keys_in_db("prod_"),
            {"prod_key_1": "prod_val_1", "prod_key_2": "prod_val_2"},
        )

    def test_search_values_in_db(self) -> None:
        """
        Testing the "search_values_in_db" method.
        :return: None
        """

        self.detti_db["test_key"] = "test_val"
        self.detti_db["prod_key_1"] = "prod_val_1"
        self.detti_db["prod_key_2"] = "prod_val_2"

        self.assertEqual(
            self.detti_db.search_values_in_db("prod_"),
            {"prod_key_1": "prod_val_1", "prod_key_2": "prod_val_2"},
        )


if __name__ == "__main__":
    unittest.main()
