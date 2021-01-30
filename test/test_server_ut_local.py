import unittest
import sys
import os
import warnings
import configparser
import subprocess
import requests
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

    proc: Optional[subprocess.Popen] = None

    def __init__(self, *args, **kwargs) -> None:
        super(DettiServerTestCases, self).__init__(*args, **kwargs)
        # Show the complete diff in case of error
        self.maxDiff: Optional[int] = None
        self.used_ut_config_file = os.path.join(
            os.path.realpath(os.path.dirname(__file__)), "detti_conf_ut.ini"
        )

    @classmethod
    def setUpClass(cls) -> None:
        """
        Running (once) before starting to run the test methods.
        It is and init method for complete UnitTests
        :return: None
        """

        warnings.filterwarnings("ignore", category=ResourceWarning)

        cls.proc: Optional[subprocess.Popen] = subprocess.Popen(
            "source venv/bin/activate && python detti_server.py --config_file {}".format(
                os.path.join(os.path.realpath(os.path.dirname(__file__)), "detti_conf_ut.ini")
            ).split(),
            executable="/bin/bash",
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Running (once) after finishing all test methods.
        It is and "destructor" method for complete UnitTests
        :return: None
        """

        if cls.proc:
            cls.proc.terminate()
            cls.proc.wait()

        config: configparser.ConfigParser = configparser.ConfigParser(allow_no_value=True)
        config.read(os.path.join(os.path.realpath(os.path.dirname(__file__)), "detti_conf_ut.ini"))
        db_file_path: str = config.get("DETTI_DB", "path_of_db")
        if os.path.isfile(db_file_path):
            os.remove(db_file_path)

    def test_get_not_exist_element(self) -> None:
        """
        Testing when the requested element is not in DB.
        :return: None
        """

        resp = requests.get("http://localhost:5000/get/not_exist")
        self.assertEqual(resp.status_code, 201)
        self.assertTrue("'not_exist' key doesn't exist in DB." in resp.text)

    def test_set_get_exist_element(self) -> None:
        """
        Testing when put an element to DB and the requested element is in DB.
        :return: None
        """

        put_resp: requests.models.Response = requests.put(
            "http://localhost:5000/set", data={"exist": "value_of_exist_key"}
        )
        self.assertEqual(put_resp.status_code, 200)
        self.assertTrue("OK" in put_resp.text)

        resp: requests.models.Response = requests.get("http://localhost:5000/get/exist")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"exist": "value_of_exist_key"})

    def test_invalid_put_to_db(self) -> None:
        """
        Testing when the data type is invalid in PUT.
        IMPORTANT:
            If the data type is not valid the PUT won't be failed.
            It can convert almost everything to string!
        :return: None
        """

        # The integer data will be converted to string and it will be the value of the key in DB.
        put_resp: requests.models.Response = requests.put(
            "http://localhost:5000/set", data={"int_data": 138}
        )
        self.assertEqual(put_resp.status_code, 200)
        self.assertTrue("OK" in put_resp.text)

        resp: requests.models.Response = requests.get("http://localhost:5000/get/int_data")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"int_data": "138"})

        # In case of list type value, the first element will be converted to string and
        # it will be the value of the key in DB.
        put_resp: requests.models.Response = requests.put(
            "http://localhost:5000/set", data={"list_data": [1, 2, 3]}
        )
        self.assertEqual(put_resp.status_code, 200)
        self.assertTrue("OK" in put_resp.text)

        resp: requests.models.Response = requests.get("http://localhost:5000/get/list_data")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"list_data": "1"})

        # In case of dict type data the first key in the inner dict will be converted to string
        # and it will be the value of the key in the DB.
        # Please be carefully it because it can cause turbulence sometimes.
        put_resp: requests.models.Response = requests.put(
            "http://localhost:5000/set", data={"dict_data": {"inner_dict_key": "inner_dict_val"}}
        )
        self.assertEqual(put_resp.status_code, 200)
        self.assertTrue("OK" in put_resp.text)

        resp: requests.models.Response = requests.get("http://localhost:5000/get/dict_data")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"dict_data": "inner_dict_key"})
