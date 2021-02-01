import unittest
import sys
import os
import warnings
import configparser
import requests
from typing import Optional

sys.path.append(os.path.join(os.path.realpath(os.path.dirname(__file__)), ".."))

# Get the path of the directory of the current file.
PATH_OF_FILE_DIR: str = os.path.realpath(os.path.dirname(__file__))


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

    @classmethod
    def setUpClass(cls) -> None:
        """
        Running (once) before starting to run the test methods.
        It is and init method for complete UnitTests
        :return: None
        """

        warnings.filterwarnings("ignore", category=ResourceWarning)

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Running (once) after finishing all test methods.
        It is and "destructor" method for complete UnitTests
        :return: None
        """

        config: configparser.ConfigParser = configparser.ConfigParser(allow_no_value=True)
        config.read(os.path.join(os.path.realpath(os.path.dirname(__file__)), "detti_conf_ut.ini"))
        db_file_path: str = config.get("DETTI_DB", "path_of_db")
        if os.path.isfile(db_file_path):
            os.remove(db_file_path)

    def test_get_not_exist_element(self) -> None:
        """
        Testing when the requested element is not in DB.
        End-point(s):
            /get/<string:db_key>
        :return: None
        """

        resp = requests.get("http://localhost:5000/get/not_exist")
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(resp.json(), {"not_exist": "The key doesn't exist in DB."})

    def test_set_get_exist_element(self) -> None:
        """
        Testing when put an element to DB and the requested element is in DB.
        End-point(s):
            /set
            /get/<string:db_key>
        :return: None
        """

        put_resp: requests.models.Response = requests.put(
            "http://localhost:5000/set", data={"exist": "value_of_exist_key"}
        )
        self.assertEqual(put_resp.status_code, 200)
        self.assertEqual(put_resp.json(), {"STATUS": "OK"})

        resp: requests.models.Response = requests.get("http://localhost:5000/get/exist")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"exist": "value_of_exist_key"})

    def test_invalid_put_to_db(self) -> None:
        """
        Testing when the data type is invalid in PUT.
        IMPORTANT:
            If the data type is not valid the PUT won't be failed.
            It can convert almost everything to string!
        End-point(s):
            /set
        :return: None
        """

        # The integer data will be converted to string and it will be the value of the key in DB.
        put_resp: requests.models.Response = requests.put(
            "http://localhost:5000/set", data={"int_data": 138}
        )
        self.assertEqual(put_resp.status_code, 200)
        self.assertEqual(put_resp.json(), {"STATUS": "OK"})

        resp: requests.models.Response = requests.get("http://localhost:5000/get/int_data")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"int_data": "138"})

        # In case of list type value, the first element will be converted to string and
        # it will be the value of the key in DB.
        put_resp: requests.models.Response = requests.put(
            "http://localhost:5000/set", data={"list_data": [1, 2, 3]}
        )
        self.assertEqual(put_resp.status_code, 200)
        self.assertEqual(put_resp.json(), {"STATUS": "OK"})

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
        self.assertEqual(put_resp.json(), {"STATUS": "OK"})

        resp: requests.models.Response = requests.get("http://localhost:5000/get/dict_data")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"dict_data": "inner_dict_key"})

    def test_ping(self) -> None:
        """
        Testing the ping to server.
        If the server is up and running the end-point should return "PONG" with 200 status code.
        If the server is down the user will get a connection error.
        End-point(s):
            /ping
        :return: None
        """

        resp: requests.models.Response = requests.get("http://localhost:5000/ping")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue("PONG" in resp.text)

    def test_search_key(self) -> None:
        """
        Searching keys in the DB based on provided key prefix.
        End-point(s):
            /search_key/<string:key_prefix>
        :return: None
        """

        put_resp: requests.models.Response = requests.put(
            "http://localhost:5000/set", data={"dev_data": "dev"}
        )
        self.assertEqual(put_resp.status_code, 200)
        self.assertEqual(put_resp.json(), {"STATUS": "OK"})

        put_resp: requests.models.Response = requests.put(
            "http://localhost:5000/set", data={"prod_key_1": "prod_val_1"}
        )
        self.assertEqual(put_resp.status_code, 200)
        self.assertEqual(put_resp.json(), {"STATUS": "OK"})

        put_resp: requests.models.Response = requests.put(
            "http://localhost:5000/set", data={"prod_key_2": "prod_val_2"}
        )
        self.assertEqual(put_resp.status_code, 200)
        self.assertEqual(put_resp.json(), {"STATUS": "OK"})

        resp: requests.models.Response = requests.get("http://localhost:5000/search_key/prod_")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"prod_key_1": "prod_val_1", "prod_key_2": "prod_val_2"})

        resp: requests.models.Response = requests.get("http://localhost:5000/search_key/nonono")
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json(), {"nonono": "Cannot find keys for prefix"})

    def test_search_val(self) -> None:
        """
        Searching values in the DB based on provided value prefix.
        End-point(s):
            /search_val/<string:value_prefix>
        :return: None
        """

        put_resp: requests.models.Response = requests.put(
            "http://localhost:5000/set", data={"dev_data": "dev"}
        )
        self.assertEqual(put_resp.status_code, 200)
        self.assertEqual(put_resp.json(), {"STATUS": "OK"})

        put_resp: requests.models.Response = requests.put(
            "http://localhost:5000/set", data={"prod_key_1": "prod_val_1"}
        )
        self.assertEqual(put_resp.status_code, 200)
        self.assertEqual(put_resp.json(), {"STATUS": "OK"})

        put_resp: requests.models.Response = requests.put(
            "http://localhost:5000/set", data={"prod_key_2": "prod_val_2"}
        )
        self.assertEqual(put_resp.status_code, 200)
        self.assertEqual(put_resp.json(), {"STATUS": "OK"})

        resp: requests.models.Response = requests.get("http://localhost:5000/search_val/prod_")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"prod_key_1": "prod_val_1", "prod_key_2": "prod_val_2"})

        resp: requests.models.Response = requests.get("http://localhost:5000/search_val/nonono")
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json(), {"nonono": "Cannot find values for prefix"})

    def test_delete_element(self) -> None:
        """
        Deleting an element from the DB.
        End-point(s):
            /delete/<string:db_key>
        :return: None
        """

        put_resp: requests.models.Response = requests.put(
            "http://localhost:5000/set", data={"to_be_deleted": "dummy"}
        )
        self.assertEqual(put_resp.status_code, 200)
        self.assertEqual(put_resp.json(), {"STATUS": "OK"})

        del_resp: requests.models.Response = requests.delete(
            "http://localhost:5000/delete/to_be_deleted"
        )
        self.assertEqual(del_resp.status_code, 200)
        self.assertEqual(del_resp.json(), {"STATUS": "OK"})

        resp: requests.models.Response = requests.get("http://localhost:5000/get/to_be_deleted")
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(resp.json(), {"to_be_deleted": "The key doesn't exist in DB."})

    def test_get_all(self) -> None:
        """
        Get all elements from the DB.
        End-point(s):
            /getall
        :return: None
        """

        put_resp: requests.models.Response = requests.put(
            "http://localhost:5000/set", data={"get_all_1": "dummy"}
        )
        self.assertEqual(put_resp.status_code, 200)
        self.assertEqual(put_resp.json(), {"STATUS": "OK"})

        put_resp: requests.models.Response = requests.put(
            "http://localhost:5000/set", data={"get_all_2": "dummy"}
        )
        self.assertEqual(put_resp.status_code, 200)
        self.assertEqual(put_resp.json(), {"STATUS": "OK"})

        resp: requests.models.Response = requests.get("http://localhost:5000/getall")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue("get_all_1" in resp.json() and "get_all_2" in resp.json())
