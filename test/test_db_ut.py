import unittest
import sys
import os
import shutil
import json
import warnings
from random import randint
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

    @classmethod
    def setUpClass(cls) -> None:
        """
        Running before tests.
        It is an init method for test methods.
        :return: None
        """

        warnings.filterwarnings("ignore", category=ResourceWarning)

    def tearDown(self) -> None:
        """
        Running after all methods.
        It is the cleaner method.
        :return: None
        """

        self.detti_db._clear_db()
        if os.path.isfile(self.detti_db.path_of_db):
            os.remove(self.detti_db.path_of_db)

    def test_exist_db_file(self) -> None:
        """
        Testing the loading an existing DB file
        :return: None
        """

        with open(self.detti_db.path_of_db, "w") as opened_db:
            json.dump({"test_key": "test_value"}, opened_db)

        self.detti_db.load_db()

    def test_not_exists_config_file(self) -> None:
        """
        Testing to get a non-exist config file.
        :return: None
        """

        random_config_file: str = "not_exist_config.ini"
        with self.assertRaises(FileNotFoundError):
            DettiDB(config_file=random_config_file)

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

        self.detti_db["test_key"] = 18
        self.assertEqual(self.detti_db["test_key"], 18)

        self.detti_db["test_key"] = 666.666
        self.assertEqual(self.detti_db["test_key"], 666.666)

        self.detti_db[12234] = 9876
        self.assertIsNone(self.detti_db[12234])

        self.detti_db["test_invalid_val"] = {"asf": 123}
        self.assertIsNone(self.detti_db["test_invalid_val"])

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

    @staticmethod
    def random_number_with_n_digits(number_of_digits) -> int:
        """
        Generating random integer with n digits.
        :param number_of_digits: Number of digits of the generated number
        :return: The generated random integer.
        """

        range_start: int = 10 ** (number_of_digits - 1)
        range_end: int = (10 ** number_of_digits) - 1
        return randint(range_start, range_end)

    def test_set_int(self) -> None:
        """
        Testing to set an integer value in DB.
        :return: None
        """

        # Testing correct setting
        self.assertTrue(self.detti_db.set_int("test_integer_val", 666))
        self.assertEqual(self.detti_db.get("test_integer_val"), 666)

        # Testing the too long key
        self.assertFalse(self.detti_db.set_int("x" * 101, 666))

        # Testing str -> float conversion
        self.assertTrue(self.detti_db.set_int("test_integer_str_val", "666"))
        self.assertEqual(self.detti_db.get("test_integer_str_val"), 666)

        # Testing the too long value
        self.assertFalse(
            self.detti_db.set_int("too_log_val", self.random_number_with_n_digits(101))
        )

        # Testing TypeError (in value)
        self.assertFalse(self.detti_db.set_int("invalid_type", ["test"]))
        self.assertIsNone(self.detti_db.get("invalid_type"))

        # Testing if key is not string
        self.assertFalse(self.detti_db.set_int(678, 666))

    def test_set_float(self) -> None:
        """
        Testing to set a float value in DB.
        :return: None
        """

        # Testing correct setting
        self.assertTrue(self.detti_db.set_float("test_float_val", 666.666))
        self.assertEqual(self.detti_db.get("test_float_val"), 666.666)

        # Testing the too long key
        self.assertFalse(self.detti_db.set_float("x" * 101, 666))

        # Testing int -> float conversion
        self.assertTrue(self.detti_db.set_float("test_float_int_val", 666))
        self.assertEqual(self.detti_db.get("test_float_int_val"), 666.0)

        # Testing str -> float conversion
        self.assertTrue(self.detti_db.set_float("test_float_str_val", "666.666"))
        self.assertEqual(self.detti_db.get("test_float_str_val"), 666.666)

        # Testing TypeError (in value)
        self.assertFalse(self.detti_db.set_float("invalid_type", ["test"]))
        self.assertIsNone(self.detti_db.get("invalid_type"))

        # Testing if key is not string
        self.assertFalse(self.detti_db.set_float(678, 666.666))

    def test_set_list(self) -> None:
        """
        Testing to set a list value in DB.
        :return: None
        """

        # Testing correct setting
        self.assertTrue(self.detti_db.set_list("test_list_val", ["a", 1]))
        self.assertEqual(self.detti_db.get("test_list_val"), ["a", 1])

        # Testing the too long key
        self.assertFalse(self.detti_db.set_list("x" * 101, ["a", 2]))

        # Testing tuple -> list conversion
        self.assertTrue(self.detti_db.set_list("test_tuple_list_val", ("a", 3)))
        self.assertEqual(self.detti_db.get("test_tuple_list_val"), ["a", 3])

        # Testing dict -> list conversion
        self.assertTrue(self.detti_db.set_list("test_dict_list_val", "abc"))
        self.assertEqual(self.detti_db.get("test_dict_list_val"), ["a", "b", "c"])

        # Testing TypeError (in value)
        self.assertFalse(self.detti_db.set_list("invalid_type", 5))
        self.assertIsNone(self.detti_db.get("invalid_type"))

        # Testing if key is not string
        self.assertFalse(self.detti_db.set_list(678, ["a", 6]))

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
        self.detti_db["prod_key_3"] = 128

        self.assertEqual(
            self.detti_db.search_keys_in_db("prod_"),
            {"prod_key_1": "prod_val_1", "prod_key_2": "prod_val_2", "prod_key_3": 128},
        )

    def test_search_values_in_db(self) -> None:
        """
        Testing the "search_values_in_db" method.
        :return: None
        """

        self.detti_db["test_key"] = "test_val"
        self.detti_db["prod_key_1"] = "prod_val_1"
        self.detti_db["prod_key_2"] = "prod_val_2"
        self.detti_db["prod_key_3"] = 128

        self.assertEqual(
            self.detti_db.search_values_in_db("prod_"),
            {"prod_key_1": "prod_val_1", "prod_key_2": "prod_val_2"},
        )

    def test_append_list(self) -> None:
        """
        Testing to append a new element to a list in DB.
        :return: None
        """

        # Set a test list type element in DB
        self.detti_db.set_list("test_list", ["a", 1])

        # Append correctly a new element to list
        self.assertTrue(self.detti_db.append_list("test_list", 666))

        self.assertEqual(self.detti_db.get("test_list"), ["a", 1, 666])

        # Try to append new element to a non-exist key
        self.assertFalse(self.detti_db.append_list("non_exist", 777))

        # Try to append a new element to a not list type element in DB.
        self.assertTrue(self.detti_db.set_float("test_float_val", 666.666))

        self.assertFalse(self.detti_db.append_list("test_float_val", 888))

    def test_is_exist(self) -> None:
        """
        Testing if an element is in DB.
        :return: None
        """

        self.detti_db["test_key"] = "test_val"

        # True should be returned if the key is in DB.
        self.assertTrue(self.detti_db.is_exist("test_key"))

        # False should be returned if the key is NOT in DB.
        self.assertFalse(self.detti_db.is_exist("test_key_2"))


if __name__ == "__main__":
    unittest.main()
