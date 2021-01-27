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

import os
import sys
import configparser
import json
import signal
from typing import Dict, Optional
from threading import Thread

# Get the path of the directory of the current file.
PATH_OF_FILE_DIR: str = os.path.join(os.path.realpath(os.path.dirname(__file__)))

# Append the path of the tools folder to find modules.
sys.path.append(os.path.join(PATH_OF_FILE_DIR, "tools"))

# Import own modules.
from color_logger import ColoredLogger  # noqa: E402

# Set the default configuration file of the DB.
DEFAULT_CONFIG: str = os.path.join(PATH_OF_FILE_DIR, "db_conf.ini")

# Set-up the main logger instance.
PATH_OF_LOG_FILE: str = os.path.join(PATH_OF_FILE_DIR, "logs", "main_log.log")
C_LOGGER: ColoredLogger = ColoredLogger(os.path.basename(__file__), log_file_path=PATH_OF_LOG_FILE)


class DettiDB(object):
    def __init__(self, config_file: str = DEFAULT_CONFIG, c_logger: ColoredLogger = None) -> None:
        self.config: configparser.ConfigParser = configparser.ConfigParser()
        self.config.read(config_file)
        self.path_of_db: str = self.config.get("DETTI_DB", "path_of_db")
        self.c_logger: ColoredLogger = c_logger if c_logger else self.set_up_default_logger()
        self.set_signal_handler()
        self.detti_db: Dict[str, str] = self.load_db()
        self.dump_thread: Optional[Thread] = None

    def __getitem__(self, key: str):
        """
        Getting item.
        :param key: Name of the key value.
        :return: The value of the item.
        """

        return self.get(key)

    def __setitem__(self, key: str, value: str):
        """
        Setting an item in the DB.
        :param key: Name of the key value.
        :param value: Value of the key.
        :return: True if the setting was successful else False
        """

        return self.set(key, value)

    def __delitem__(self, key: str):
        """
        Deleting item from DB.
        :param key: Name of the key value.
        :return: True if the deleting was successful else False
        """
        return self.delete(key)

    @staticmethod
    def set_up_default_logger() -> ColoredLogger:
        """
        Set up a default logger if it is not provided in instance.
        :return: ColoredLogger object
        """

        return ColoredLogger(os.path.basename(__file__), log_file_path=PATH_OF_LOG_FILE)

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

    def get(self, db_key: str) -> Optional[str]:
        """
        Providing the value of a key.
        The method returns None if the key doesn't exist in the DB.
        :param db_key: Related key.
        :return: The value of the key as a string.
        """

        self.c_logger.info("Starting to the the '{}' element.".format(db_key))

        try:
            value_of_key: str = self.detti_db[db_key]
            self.c_logger.ok("Successfully get the value of '{}': {}".format(db_key, value_of_key))
            return value_of_key
        except KeyError:
            self.c_logger.warning("The '{}' key doesn't exist in the DB.".format(db_key))
            return None
        except Exception as unexpected_error:
            self.c_logger.error(
                "Unexpected error happened during the get an element. ERROR:\n{}".format(
                    unexpected_error
                )
            )
            raise unexpected_error

    def set(self, db_key: str, db_value: str) -> bool:
        """
        Setting a new item in the DB.
        :param db_key: Key of the item.
        :param db_value: Value of the key.
        :return: True if the operation is success else False.
        """

        self.c_logger.info("Starting to set the '{}:{}' key-value pair".format(db_key, db_value))

        if isinstance(db_key, str) and isinstance(db_value, str):
            if len(db_key) > self.config.getint("DETTI_DB", "len_of_key"):
                self.c_logger.warning(
                    "The length of key is too long. The value won't be stored! Max. len: {}".format(
                        self.config.getint("DETTI_DB", "len_of_key")
                    )
                )
                return False
            elif len(db_value) > self.config.getint("DETTI_DB", "len_of_val"):
                self.c_logger.warning(
                    "The length of key is too long. The value won't be stored! Max len: {}".format(
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

    def dump_json(self) -> None:
        """
        Dump the dict object to the Json file in case of DB changing.
        It is performed on multithreading.
        :return: None
        """

        with open(self.path_of_db, "wt") as opened_db:
            self.dump_thread: Thread = Thread(target=json.dump, args=(self.detti_db, opened_db))
            self.dump_thread.start()
            self.dump_thread.join()

    def search_in_db(self, key_prefix: str) -> Dict[str, str]:
        """
        Searching the keys based on the provided prefix.
        The return list contains the matched keys and values in a dict
        :param key_prefix: Prefix of the key
        :return: Dict[str, str] The found key-value pairs
        """

        self.c_logger.info("Starting to search in DB based on '{}' prefix".format(key_prefix))

        return_dict: Dict[str, str] = {}
        key: str
        value: str

        for key, value in self.detti_db.items():
            if key.startswith(key_prefix):
                self.c_logger.debug(
                    "Found key-value pair for '{}' prefix: {}:{}".format(key_prefix, key, value)
                )
                return_dict[key]: str = value

        self.c_logger.ok("Successfully run the searching in the DB.")

        return return_dict

    def set_signal_handler(self) -> None:
        """
        Set a signal handler.
        It is important if the script gets an interrupt signal during updating the DB.
        The threads should be joined before exit.
        :return: None
        """

        self.c_logger.debug("Starting to setup the Signal handler.")

        def sigterm_handler(*args):
            if self.dump_thread:
                self.dump_thread.join()
            sys.exit(1)

        signal.signal(signal.SIGTERM, sigterm_handler)
        signal.signal(signal.SIGINT, sigterm_handler)


if __name__ == "__main__":
    detti_db = DettiDB()
    detti_db["test"] = "OK"
    detti_db["as"] = "ppp"
    detti_db["teso"] = "uuuu"
    print(detti_db["test"])
    print(detti_db.search_in_db("te"))
