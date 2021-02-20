#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# BSD 3-Clause License
#
# Copyright (c) 2021, Milan Balazs
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Lightweight Json based key-value DataBase.
"""

import os
import sys
import configparser
import json
import signal
from datetime import datetime
from typing import Dict, Optional, Union, Any
from threading import Thread, Lock

# Get the path of the directory of the current file.
PATH_OF_FILE_DIR: str = os.path.realpath(os.path.dirname(__file__))

# Append the path of the tools folder to find modules.
sys.path.append(os.path.join(PATH_OF_FILE_DIR, "tools"))

# Import own modules.
from color_logger import ColoredLogger  # noqa: E402

# Set the default configuration file of the DB.
DEFAULT_CONFIG: str = os.path.join(PATH_OF_FILE_DIR, "detti_conf.ini")

LOG_LEVELS: Dict[str, int] = {
    "CRITICAL": 50,
    "ERROR": 40,
    "WARNING": 30,
    "INFO": 20,
    "DEBUG": 10,
}


# Set-up the main logger instance.
PATH_OF_LOG_FILE: str = os.path.join(
    PATH_OF_FILE_DIR, "logs", "detti_db_{}.log".format(datetime.now().strftime("%Y%m%d_%H%M%S"))
)
C_LOGGER: ColoredLogger = ColoredLogger(os.path.basename(__file__), log_file_path=PATH_OF_LOG_FILE)


class DettiDB(object):
    def __init__(self, config_file: str = DEFAULT_CONFIG, c_logger: ColoredLogger = None) -> None:
        self.c_logger: ColoredLogger = c_logger if c_logger else self.set_up_default_logger()
        self.config: configparser.ConfigParser = configparser.ConfigParser()
        self.check_config_file(config_file)
        self.config.read(config_file)
        self.set_up_default_logger(log_level=self.config.get("DETTI_DB", "log_level"))
        self.path_of_db: str = os.path.abspath(self.config.get("DETTI_DB", "path_of_db"))
        self.set_signal_handler()
        self.detti_db: Dict[str, str] = self.load_db()
        self.dump_thread: Optional[Thread] = None
        self.lock: Lock = Lock()

    def __getitem__(self, key: str) -> Optional[Union[str, int, float]]:
        """
        Getting item.
        :param key: Name of the key value.
        :return: The value of the item.
        """

        return self.get(key)

    def __setitem__(self, key: str, value: Union[str, int, float, list]) -> bool:
        """
        Setting an item in the DB.
        :param key: Name of the key value.
        :param value: Value of the key.
        :return: True if the setting was successful else False
        """

        return self._set(key, value)

    def __delitem__(self, key: str) -> bool:
        """
        Deleting item from DB.
        :param key: Name of the key value.
        :return: True if the deleting was successful else False
        """
        return self.delete(key)

    def check_config_file(self, config_file_path: str) -> None:
        """
        Checking the getting config file.
        :return: None
        """

        self.c_logger.info("Starting to check the getting config file.")

        if not os.path.isfile(config_file_path):
            error_msg: str = "The getting config file doesn't exist: {}".format(config_file_path)
            self.c_logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        file_permissions: str = oct(os.stat(config_file_path).st_mode & 0o777)

        if file_permissions != 0o600:
            self.c_logger.warning(
                "The getting config file's permission is not 600! "
                "Recommended to change it. "
                "Current permissions: {}".format(file_permissions)
            )

        self.c_logger.ok("The config file checking has been done!")

    def set_up_default_logger(self, log_level: Optional[str] = None) -> Optional[ColoredLogger]:
        """
        Set up a default logger if it is not provided in instance.
        :return: ColoredLogger object
        """

        if log_level:
            self.c_logger.console.setLevel(LOG_LEVELS[log_level.upper()])
            return

        return ColoredLogger(
            os.path.basename(__file__),
            console_level=LOG_LEVELS["DEBUG"],
            log_file_path=PATH_OF_LOG_FILE,
        )

    def __creating_dir_structure_for_file(self, path_of_file: str) -> None:
        """
        Creating directory structure for a file if it is not existing.
        :return: None
        """

        self.c_logger.info("Starting to check if the directory structure exists.")

        if not os.path.exists(os.path.dirname(path_of_file)) and os.path.dirname(path_of_file):
            self.c_logger.warning("The directory structure of provided DB file doesn't exist")
            self.c_logger.info("Starting to try to creating the directory structure of DB file.")
            os.makedirs(os.path.dirname(path_of_file), exist_ok=True)
            self.c_logger.ok("Successfully created the directory structure of DB file.")
        else:
            self.c_logger.ok("The directory structure of DB file exist.")

    def load_db(self) -> Dict[str, str]:
        """
        Loading the DB based on the provided confing file.
        If the DB doesn't exist the method creates it.
        If the DB exists but it is empty the methot returns an empty Dict object.
        :return: Dict[str, str]. The key-value pairs from DB file
        """

        self.c_logger.info("Starting to load the DB.")

        if not os.path.isfile(self.path_of_db):
            self.c_logger.warning("The '{}' DB file doesn't exist.".format(self.path_of_db))
            # Creating the directory structure in it is not existing
            self.__creating_dir_structure_for_file(self.path_of_db)
            # Creating new DB if it is not exist
            with open(self.path_of_db, "w"):
                # Only the owner has permissions for DB file
                os.chmod(self.path_of_db, 0o600)
            self.c_logger.ok("The new '{}' DB has been created.".format(self.path_of_db))
            return {}
        self.c_logger.debug("The DB file exists.")
        try:
            loaded_db: Dict[str, str] = json.load(open(self.path_of_db, "rt"))
            self.c_logger.ok("The '{}' DB has been loaded.".format(self.path_of_db))
            return loaded_db
        except ValueError as val_error:
            # Checking if file is empty
            if os.stat(self.path_of_db).st_size == 0:
                self.c_logger.warning("The '{}' DB is empty.".format(self.path_of_db))
                return {}
            else:
                self.c_logger.error(
                    "ValueError happened during the DB loading. ERROR:\n{}".format(val_error)
                )
                raise val_error
        except Exception as unexpected_error:
            self.c_logger.error(
                "Unexpected error happened during the DB loading. ERROR:\n{}".format(
                    unexpected_error
                )
            )
            raise unexpected_error

    def get(self, db_key: str) -> Optional[Union[str, int, float]]:
        """
        Providing the value of a key.
        The method returns None if the key doesn't exist in the DB.
        :param db_key: Related key.
        :return: The value of the key as a string.
        """

        self.c_logger.info("Starting to get the '{}' element.".format(db_key))

        try:
            value_of_key: Union[str, int, float] = self.detti_db[db_key]
            self.c_logger.ok("Successfully get the value of '{}': {}".format(db_key, value_of_key))
            return value_of_key
        except KeyError:
            self.c_logger.warning("The '{}' key doesn't exist in the DB.".format(db_key))
            return None
        except Exception as unexpected_error:  # pragma: no cover
            self.c_logger.error(
                "Unexpected error happened during the get an element. ERROR:\n{}".format(
                    unexpected_error
                )
            )
            raise unexpected_error

    def get_all(self) -> Dict[str, Union[str, int, float]]:
        """
        Providing the all elements from DB.
        The method returns None if the DB is empty.
        :return: The content of DB in dict or empty dict if the DB is empty.
        """

        self.c_logger.info("Starting to the get the all elements.")

        if not self.detti_db:
            self.c_logger.warning("The DB is empty")
            return {}
        self.c_logger.ok("The DB has content and it's returned.")
        return self.detti_db

    def _set(self, db_key: str, db_value: Union[str, int, float, list]) -> bool:
        """
        Decide what type of setting is needed and call the proper method.
        :param db_key: Key of the item.
        :param db_value: Value of the key.
        :return: True if the operation is success else False.
        """

        self.c_logger.info("Starting to set the '{}:{}' key-value pair".format(db_key, db_value))

        if not isinstance(db_key, str):
            self.c_logger.warning("The key is not string! The value won't be stored!")
            return False

        if isinstance(db_value, str):
            self.set(db_key, db_value)
        elif isinstance(db_value, int):
            self.set_int(db_key, db_value)
        elif isinstance(db_value, float):
            self.set_float(db_key, db_value)
        elif isinstance(db_value, list):
            self.set_list(db_key, db_value)
        else:
            self.c_logger.warning(
                "The getting value type is not supported ({}). "
                "The value won't be stored.".format(type(db_value))
            )
            return False

    def set(self, db_key: str, db_value: str) -> bool:
        """
        Setting a new item in the DB (string).
        This is the default setting of DB.
        :param db_key: Key of the item.
        :param db_value: Value of the key.
        :return: True if the operation is success else False.
        """

        self.c_logger.info(
            "Starting to set the '{}:{}' string key-value pair".format(db_key, db_value)
        )

        try:
            self.c_logger.debug("Try to convert the getting value to string.")
            db_value: str = str(db_value)
        except TypeError:
            self.c_logger.warning("The value is not string and it cannot be casted to string.")
            return False

        if isinstance(db_key, str) and isinstance(db_value, str):
            if len(db_key) > self.config.getint("DETTI_DB", "len_of_key"):
                self.c_logger.warning(
                    "The length of key is too long. "
                    "The value won't be stored! Max. len: {}".format(
                        self.config.getint("DETTI_DB", "len_of_key")
                    )
                )
                return False
            elif len(db_value) > self.config.getint("DETTI_DB", "len_of_val"):
                self.c_logger.warning(
                    "The length of value is too long. "
                    "The value won't be stored! Max len: {}".format(
                        self.config.getint("DETTI_DB", "len_of_val")
                    )
                )
                return False
            db_key: str = db_key.strip()
            db_value: str = db_value.strip()
            self.detti_db[db_key]: str = db_value
            self.dump_json()
            self.c_logger.ok(
                "'{}:{}' key-value pair has been stored successfully.".format(db_key, db_value)
            )
            return True
        else:
            self.c_logger.warning("The key or the value is not string! The value won't be stored!")
            return False

    def set_int(self, db_key: str, db_value: int) -> bool:
        """
        Setting a new integer item in the DB.
        :param db_key: Key of the item.
        :param db_value: Value of the key.
        :return: True if the operation is success else False.
        """

        self.c_logger.info(
            "Starting to set the '{}:{}' integer key-value pair".format(db_key, db_value)
        )

        try:
            self.c_logger.debug("Try to convert the getting value to integer.")
            db_value: int = int(db_value)
        except TypeError:
            self.c_logger.warning("The value is not integer and it cannot be casted to integer.")
            return False

        if isinstance(db_key, str) and isinstance(db_value, int):
            if len(db_key) > self.config.getint("DETTI_DB", "len_of_key"):
                self.c_logger.warning(
                    "The length of key is too long. "
                    "The value won't be stored! Max. len: {}".format(
                        self.config.getint("DETTI_DB", "len_of_key")
                    )
                )
                return False
            # TODO: Introduce new parameter to config file about size of integers.
            elif len(str(db_value)) > self.config.getint("DETTI_DB", "len_of_val"):
                self.c_logger.warning(
                    "The length of value is too long. "
                    "The value won't be stored! Max len: {}".format(
                        self.config.getint("DETTI_DB", "len_of_val")
                    )
                )
                return False
            db_key: str = db_key.strip()
            self.detti_db[db_key]: int = db_value
            self.dump_json()
            self.c_logger.ok(
                "'{}:{}' integer key-value pair has been stored successfully.".format(
                    db_key, db_value
                )
            )
            return True
        else:
            self.c_logger.warning("The key is not string! The value won't be stored!")
            return False

    def set_float(self, db_key: str, db_value: float) -> bool:
        """
        Setting a new float item in the DB.
        :param db_key: Key of the item.
        :param db_value: Value of the key.
        :return: True if the operation is success else False.
        """

        self.c_logger.info(
            "Starting to set the '{}:{}' float key-value pair".format(db_key, db_value)
        )

        try:
            self.c_logger.debug("Try to convert the getting value to float.")
            db_value: float = float(db_value)
        except TypeError:
            self.c_logger.warning("The value is not float and it cannot be casted to float.")
            return False

        if isinstance(db_key, str) and isinstance(db_value, float):
            if len(db_key) > self.config.getint("DETTI_DB", "len_of_key"):
                self.c_logger.warning(
                    "The length of key is too long. "
                    "The value won't be stored! Max. len: {}".format(
                        self.config.getint("DETTI_DB", "len_of_key")
                    )
                )
                return False
            # TODO: Introduce new parameter to config file about size of float.
            elif len(str(db_value)) > self.config.getint("DETTI_DB", "len_of_val"):
                self.c_logger.warning(
                    "The length of value is too long. "
                    "The value won't be stored! Max len: {}".format(
                        self.config.getint("DETTI_DB", "len_of_val")
                    )
                )
                return False
            db_key: str = db_key.strip()
            self.detti_db[db_key]: float = db_value
            self.dump_json()
            self.c_logger.ok(
                "'{}:{}' float key-value pair has been stored successfully.".format(
                    db_key, db_value
                )
            )
            return True
        else:
            self.c_logger.warning("The key is not string! The value won't be stored!")
            return False

    def set_list(self, db_key: str, db_value: list) -> bool:
        """
        Setting a new list item in the DB.
        :param db_key: Key of the item.
        :param db_value: Value of the key.
        :return: True if the operation is success else False.
        """

        self.c_logger.info(
            "Starting to set the '{}:{}' list key-value pair".format(db_key, db_value)
        )

        try:
            self.c_logger.debug("Try to convert the getting value to list.")
            db_value: list = list(db_value)
        except TypeError:
            self.c_logger.warning("The value is not list and it cannot be casted to list.")
            return False

        if isinstance(db_key, str) and isinstance(db_value, list):
            if len(db_key) > self.config.getint("DETTI_DB", "len_of_key"):
                self.c_logger.warning(
                    "The length of key is too long. "
                    "The value won't be stored! Max. len: {}".format(
                        self.config.getint("DETTI_DB", "len_of_key")
                    )
                )
                return False
            # TODO: Introduce new parameter to config file about size of list.
            elif len(str(db_value)) > self.config.getint("DETTI_DB", "len_of_val"):
                self.c_logger.warning(
                    "The length of value is too long. "
                    "The value won't be stored! Max len: {}".format(
                        self.config.getint("DETTI_DB", "len_of_val")
                    )
                )
                return False
            db_key: str = db_key.strip()
            self.detti_db[db_key]: list = db_value
            self.dump_json()
            self.c_logger.ok(
                "'{}:{}' list key-value pair has been stored successfully.".format(db_key, db_value)
            )
            return True
        else:
            self.c_logger.warning("The key is not string! The value won't be stored!")
            return False

    def append_list(self, db_key: str, db_val: Any):
        """
        Append a new element for a list in the DB.
        :param db_key: Key of the list element in DB.
        :param db_val: The appended value.
        :return: True if the operation is success else False.
        """

        self.c_logger.info(
            "Starting to append the '{}' item to '{}' list in DB".format(db_val, db_key)
        )

        if db_key not in self.detti_db:
            self.c_logger.warning("The '{}' key is not in DB.".format(db_key))
            return False

        if not isinstance(self.detti_db[db_key], list):
            self.c_logger.warning(
                "The value of '{}' key is not a list. Cannot append element".format(db_key)
            )
            return False

        self.detti_db[db_key].append(db_val)

        self.dump_json()

        self.c_logger.ok("'{}' successfully append to '{}' list".format(db_val, db_key))

        return True

    def delete(self, db_key: str) -> bool:
        """
        Deleting an item from the DB.
        :param db_key: Key of the item.
        :return: True if the operation is success else False.
        """

        self.c_logger.info("Starting to remove the '{}' item from DB".format(db_key))

        if db_key not in self.detti_db:
            self.c_logger.warning("The '{}' key is not in DB! It cannot be removed".format(db_key))
            return False
        del self.detti_db[db_key]
        self.dump_json()
        self.c_logger.ok("The '{}' item has been removed successfully from DB.".format(db_key))
        return True

    def _clear_db(self) -> None:
        """
        It is a really dangerous method.
        This method clears the complete DB.
        ALL DATA WILL BE DELETED FROM DB AND IT IS NOT REVOCABLE!
        :return: True if the operation is success else False.
        """

        self.c_logger.info("Starting to clear the complete DB")
        self.detti_db: dict = {}
        self.dump_json()
        self.c_logger.ok("The DB has been cleared successfully.")

    def dump_json(self) -> None:
        """
        Dump the dict object to the Json file in case of DB changing.
        It is performed on multithreading.
        :return: None
        """

        with self.lock:
            with open(self.path_of_db, "wt") as opened_db:
                self.dump_thread: Thread = Thread(target=json.dump, args=(self.detti_db, opened_db))
                self.dump_thread.start()
                self.dump_thread.join()

    def search_keys_in_db(self, key_prefix: str) -> Dict[str, str]:
        """
        Searching the keys based on the provided prefix.
        The return list contains the matched keys and values in a dict
        :param key_prefix: Prefix of the key
        :return: Dict[str, str] The found key-value pairs
        """

        self.c_logger.info("Starting to search keys in DB based on '{}' prefix".format(key_prefix))

        return_dict: Dict[str, str] = {}
        key: str
        value: str

        for key, value in self.detti_db.items():
            if key.startswith(key_prefix):
                self.c_logger.debug(
                    "Found key-value pair for '{}' key prefix: {}:{}".format(key_prefix, key, value)
                )
                return_dict[key]: str = value

        self.c_logger.ok("Successfully run the key searching in the DB.")

        return return_dict

    def search_values_in_db(self, value_prefix: str) -> Dict[str, str]:
        """
        Searching the values based on the provided prefix.
        The return list contains the matched keys and values in a dict
        :param value_prefix: Prefix of the value
        :return: Dict[str, str] The found key-value pairs
        """

        self.c_logger.info(
            "Starting to search values in DB based on '{}' prefix".format(value_prefix)
        )

        return_dict: Dict[str, str] = {}
        key: str
        value: str

        for key, value in self.detti_db.items():
            if not isinstance(value, str):
                continue
            if value.startswith(value_prefix):
                self.c_logger.debug(
                    "Found key-value pair for '{}' value prefix: {}:{}".format(
                        value_prefix, key, value
                    )
                )
                return_dict[key]: str = value

        self.c_logger.ok("Successfully run the value searching in the DB.")

        return return_dict

    def is_exist(self, db_key: str) -> bool:
        """
        Checking if key is in DB.
        :param db_key: Key of the item.
        :return: True if the item exist else False.
        """

        self.c_logger.info("Starting to check if '{}' key exists in DB.".format(db_key))

        return db_key in self.detti_db

    def set_signal_handler(self) -> None:
        """
        Set a signal handler.
        It is important if the script gets an interrupt signal during updating the DB.
        The threads should be joined before exit.
        :return: None
        """

        self.c_logger.debug("Starting to setup the Signal handler.")

        def sigterm_handler(*args):  # pragma: no cover
            if self.dump_thread:
                self.dump_thread.join()
            sys.exit(1)

        signal.signal(signal.SIGTERM, sigterm_handler)
        signal.signal(signal.SIGINT, sigterm_handler)


if __name__ == "__main__":
    detti_db = DettiDB()
