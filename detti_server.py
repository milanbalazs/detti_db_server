"""
Server for the Detti DB.

End-points:
    /get/<string:db_key>
        Providing the key-value pair based on getting key. {key: value}
    /set
        Setting/updating key-value pair in the DB.
        Eg.: >> curl http://localhost:5000/set -d "test_key=test_val" -X PUT
    /search_key/<string:key_prefix>
        Searching keys in the DB based on provided key prefix. {key: value, key: value}
    /search_val/<string:value_prefix>
        Searching values in the DB based on provided value prefix. {key: value, key: value}
    /delete/<string:db_key>
        Deleting an element from the DB.
        Eg.: curl http://localhost:5000/delete/test_key -X DELETE
    /ping
        Checking if the server is running.
    /getall
        Providing all elements from the DB. {key: value, key: value}

Limiter:
    There is a limiter in the server to avoid the overload.
    The request limit threshold can be set in the config file in different units.
    Example:
        >> curl http://localhost:5000/get/test_key
        > "'test_key' key doesn't exist in DB."
        ...
        ...
        >> curl http://localhost:5000/get/test_key
        > {
                "message": "5 per 1 minute"
          }

"""

import os
import sys
import configparser
from functools import wraps
from typing import Union, Optional, Dict, List
from flask import Flask, request
from flask_restful import Resource, Api, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

# Get the path of the directory of the current file.
PATH_OF_FILE_DIR: str = os.path.realpath(os.path.dirname(__file__))

# Append the path of the tools folder to find modules.
sys.path.append(PATH_OF_FILE_DIR)

from detti_db import DettiDB  # noqa: E402

detti_db: DettiDB = DettiDB()

app: Flask = Flask(__name__)
api: Api = Api(app)

config: configparser.ConfigParser = configparser.ConfigParser(allow_no_value=True)
config.read(os.path.join(os.path.realpath(os.path.dirname(__file__)), "detti_conf.ini"))

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=[
        "{} per day".format(config.get("SERVER", "day_limit")),
        "{} per hour".format(config.get("SERVER", "hour_limit")),
        "{} per minute".format(config.get("SERVER", "min_limit")),
        "{} per second".format(config.get("SERVER", "sec_limit")),
    ],
)


class User(object):
    """
    This class works as a data collector for the registered users.
    Basically the User/Password pairs come from the config file.
    If the User/Password pair is not set in the config file the Auth is not needed.
    """

    def __init__(self, user_id: int, username: str, password: str) -> None:
        """
        Init method of 'User' class.
        :param user_id: Id of the registered user.
        :param username: Name of the user.
        :param password: Password of the user.
        """

        self.id: int = user_id
        self.username: str = username
        self.password: str = password

    def __str__(self) -> str:
        """
        Return the User ID.
        :return: User ID as a string.
        """

        return "User(id='{}')".format(self.id)


# More users can be registred if it is needed.
# Current only one user is possible and the credentials comes from the config file.
# In default the Auth it not needed. Please be careful to set it!
users: List[User] = [
    User(1, config.get("SERVER", "user"), config.get("SERVER", "password"))
]

username_table: dict = {u.username: u for u in users}
userid_table: dict = {u.id: u for u in users}
app.config["SECRET_KEY"] = "super-secret"


def authenticate(username: str, password: str) -> User:
    """
    Authentication function.
    This function is passed to JWT object as authentication header.
    :param username: Name of the user as a string.
    :param password: Password of the user as a string.
    :return: Return the User object.
    """

    user: User = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode("utf-8"), password.encode("utf-8")):
        return user


def identity(payload: dict) -> Optional[int]:
    """
    Identity handler function.
    This function is passed to JWT object as identity handler.
    :param payload: Payload of request.
    :return: ID of the user or None if the user is not in the table.
    """

    user_id = payload["identity"]
    return userid_table.get(user_id, None)


jwt: JWT = JWT(app, authenticate, identity)


def checkuser(func):
    """
    Global decorator to check the user authentication in the RESTFUL API Classes.
    :param func: Reference of the decorated function.
    :return: Return the reference of the inner function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        Inner function of the global decorator.
        This inner wrapper function calls the decorated function/method and handles the parameters.
        :param args: Arguments of the decorated function/method.
        :param kwargs: Keyword-arguments of the decorated function/method.
        :return: Return the called decorated function or abort with 401 status-code.
        """

        if current_identity.username in username_table.keys():
            return func(*args, **kwargs)
        return abort(401)

    return wrapper


DECORATORS = (
    [checkuser, jwt_required()]
    if (config.get("SERVER", "user") and config.get("SERVER", "password"))
    else []
)


class GetItem(Resource):
    """
    This class contains the all GET related implementations.
    """

    decorators = DECORATORS

    @staticmethod
    def get(db_key: str) -> Union[Dict[str, str], tuple]:
        """
        This get method provides the value of the key and the key itself in a dict.
        If the key doesn't exist in the DB, the method provides an error message
        with 201 status code.
        Eg.:
            >> curl http://localhost:5000/get/exist
            > {"exist": "value_of_exist_key"}
            >> curl http://localhost:5000/get/doesnt_exist
            > "'doesnt_exist' key doesn't exist in DB."

        :param db_key: The related key's name.
        :return: The value of the key or an error message as string or tuple.
        """

        value: Optional[str] = detti_db[db_key]
        if not value:
            return "'{}' key doesn't exist in DB.".format(db_key), 201
        return {db_key: detti_db[db_key]}


class SetItem(Resource):
    """
    This class contains the all value setting in DB related implementations.
    """

    decorators = DECORATORS

    @staticmethod
    def put() -> str:
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


class SearchKeys(Resource):
    """
    This class contains the all searching in DB related implementations.
    """

    decorators = DECORATORS

    @staticmethod
    def get(key_prefix: str) -> Union[tuple, Dict[str, str]]:
        """
        You can search keys in the DB with this method.
        It uses the input parameter as a prefix of the keys.
        Eg.:
            >> curl http://localhost:5000/set -d "test_key=test_val" -X PUT
            > "OK"
            >> curl http://localhost:5000/set -d "prod_key_1=prod_val_1" -X PUT
            >  "OK"
            >> curl http://localhost:5000/set -d "prod_key_2=prod_val_2" -X PUT
            >  "OK"
            >> curl http://localhost:5000/search_key/prod_
            > {
                    "prod_key_1": "prod_val_1",
                    "prod_key_2": "prod_val_2"
                }
            >> curl http://localhost:5000/search_key/not_exist
            >"Cannot find keys based on 'not_exist' prefix"

        :param key_prefix: Prefix of the searched keys.
        :return: The found key-value pairs in a dict if found any
                 else an error message with a 201 status code.
        """

        values: Dict[str, str] = detti_db.search_keys_in_db(key_prefix)
        if not values:
            return "Cannot find keys based on '{}' prefix".format(key_prefix), 201
        return values


class SearchValues(Resource):
    """
    This class contains the all value searching in DB related implementations.
    """

    decorators = DECORATORS

    @staticmethod
    def get(value_prefix: str) -> Union[tuple, Dict[str, str]]:
        """
        You can search values in the DB with this method.
        It uses the input parameter as a prefix of the values.
        Eg.:
            >> curl http://localhost:5000/set -d "test_key=test_val" -X PUT
            > "OK"
            >> curl http://localhost:5000/set -d "prod_key_1=prod_val_1" -X PUT
            >  "OK"
            >> curl http://localhost:5000/set -d "prod_key_2=prod_val_2" -X PUT
            >  "OK"
            >> curl http://localhost:5000/search_val/prod_
            > {
                    "prod_key_1": "prod_val_1",
                    "prod_key_2": "prod_val_2"
                }
            >> curl http://localhost:5000/search_val/not_exist
            > "Cannot find values based on 'not_exist' prefix"

        :param value_prefix: Prefix of the searched values.
        :return: The found key-value pairs in a dict if found any
                 else an error message with a 201 status code.
        """

        values: Dict[str, str] = detti_db.search_values_in_db(value_prefix)
        if not values:
            return "Cannot find values based on '{}' prefix".format(value_prefix), 201
        return values


class DeleteItem(Resource):
    """
    This class contains the all deleting from DB related implementations.
    """

    decorators = DECORATORS

    @staticmethod
    def delete(db_key: str) -> str:
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


class PingServer(Resource):
    """
    This class contains the server ping related implementations.
    """

    decorators = DECORATORS

    @staticmethod
    def get() -> str:
        """
        If the server is up and running this method provides "PONG".
        If the server is not alive and request will be failed.
        Eg.:
            Success:
                >> curl http://localhost:5000/ping
                > "PONG"
            Failed (Status code: 7):
                >> curl http://localhost:5000/ping
                > curl: (7) Failed to connect to localhost port 5000: Kapcsolat elutasítva
        :return: "PONG" as string
        """

        return "PONG"


class GetAll(Resource):
    """
    This class contains the get all elements implementations.
    """

    decorators = DECORATORS

    @staticmethod
    def get() -> Dict[str, str]:
        """
        Providing the all elements of the DB.
        If the DB is empty, an empty dict will be returned.
        Eg.:
            >> curl http://localhost:5000/set -d "test_key=test_val" -X PUT
            > "OK"
            >> curl http://localhost:5000/set -d "test_key_1=test_val_1" -X PUT
            > "OK"
            >> curl http://localhost:5000/getall
            > {
                    "test_key": "test_val",
                    "test_key_1": "test_val_1"
              }

        :return: The content of DB in dict or empty dict if the DB is empty.
        """

        return detti_db.get_all()


api.add_resource(GetItem, "/get/<string:db_key>")
api.add_resource(SetItem, "/set")
api.add_resource(SearchKeys, "/search_key/<string:key_prefix>")
api.add_resource(SearchValues, "/search_val/<string:value_prefix>")
api.add_resource(DeleteItem, "/delete/<string:db_key>")
api.add_resource(PingServer, "/ping")
api.add_resource(GetAll, "/getall")

if __name__ == "__main__":
    app.run(
        host=config.get("SERVER", "host"),
        port=config.get("SERVER", "port"),
        debug=config.getboolean("SERVER", "debug"),
    )
