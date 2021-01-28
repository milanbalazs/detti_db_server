import os
import sys
from typing import Union, Optional, Dict
from flask import Flask, request
from flask_restful import Resource, Api

# Get the path of the directory of the current file.
PATH_OF_FILE_DIR: str = os.path.join(os.path.realpath(os.path.dirname(__file__)))

# Append the path of the tools folder to find modules.
sys.path.append(PATH_OF_FILE_DIR)

from detti_db import DettiDB  # noqa: E402

detti_db: DettiDB = DettiDB()
app: Flask = Flask(__name__)
api: Api = Api(app)


class GetItem(Resource):
    """
    This class contains the all GET related implementations.
    """

    def get(self, db_key: str) -> Union[str, tuple]:
        """
        This get method provides the value of the key based on the end-point.
        If the key doesn't exist in the DB, the method provides an error message
        with 201 status code.
        Eg.:
            >> curl http://localhost:5000/get/exist
            > "value_of_exist_key"
            >> curl http://localhost:5000/get/doesnt_exist
            > "'doesnt_exist' key doesn't exist in DB."

        :param db_key: The related key's name.
        :return: The value of the key or an error message as string or tuple.
        """

        value: Optional[str] = detti_db[db_key]
        if not value:
            return "'{}' key doesn't exist in DB.".format(db_key), 201
        return detti_db[db_key]


class SetItem(Resource):
    """
    This method contains the all value setting in DB related implementations.
    """

    def put(self) -> str:
        """
        This method can set/update an item in the DB.
        If the operation is success, the method returns "OK" with 200 status code (default).
        Eg.:
            >> curl http://localhost:5000/set -d "test_key=test_val" -X PUT
            > "OK"
            >> curl http://localhost:5000/get/test_key
            > "test_val"

        :return: "OK" as string
        """

        key: str
        value: str
        for key, value in request.form.items():
            detti_db[key]: str = value
        return "OK"


class SearchItem(Resource):
    """
    This method contains the all searching in DB related implementations.
    """

    def get(self, key_prefix: str) -> Union[tuple, Dict[str, str]]:
        """
        You can search in the DB with this method.
        It uses the input parameter as a prefix of the keys.
        Eg.:
            >> curl http://localhost:5000/set -d "test_key=test_val" -X PUT
            > "OK"
            >> curl http://localhost:5000/set -d "prod_key_1=prod_val_1" -X PUT
            >  "OK"
            >> curl http://localhost:5000/set -d "prod_key_2=prod_val_2" -X PUT
            >  "OK"
            >> curl http://localhost:5000/search/prod_
            > {
                    "prod_key_1": "prod_val_1",
                    "prod_key_2": "prod_val_2"
                }

        :param key_prefix: Prefix of the searched keys.
        :return: The found key-value pairs in a dict if found any
                 else an error message with a 201 status code.
        """

        values: Dict[str, str] = detti_db.search_in_db(key_prefix)
        if not values:
            return "Cannot find keys based on '{}' prefix".format(key_prefix), 201
        return detti_db.search_in_db(key_prefix)


class DeleteItem(Resource):
    """
    This method contains the all deleting from DB related implementations.
    """

    def delete(self, db_key: str) -> str:
        """
        You can delete elements from the DB with this method.
        Eg.:
            >> curl http://localhost:5000/set -d "test_key=test_val" -X PUT
            > "OK"
            >> curl http://localhost:5000/get/test_key
            > "test_val"
            >> curl http://localhost:5000/delete/test_key -X DELETE
            > "OK"
            >> curl http://localhost:5000/get/test_key
            > "'test_key' key doesn't exist in DB."

        :param db_key: Name of the deleted key.
        :return: "OK" as a string.
        """

        del detti_db[db_key]
        return "OK"


api.add_resource(GetItem, "/get/<string:db_key>")
api.add_resource(SetItem, "/set")
api.add_resource(SearchItem, "/search/<string:key_prefix>")
api.add_resource(DeleteItem, "/delete/<string:db_key>")

if __name__ == "__main__":
    app.run(debug=True)
