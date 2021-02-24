import os
import sys

# Get the path of the directory of the current file.
PATH_OF_FILE_DIR: str = os.path.realpath(os.path.dirname(__file__))

# Append the path of the tools folder to find modules.
sys.path.append(os.path.join(PATH_OF_FILE_DIR, ".."))

from detti_db import DettiDB  # noqa: E40

detti_db: DettiDB = DettiDB()

# setters
detti_db["test_key"] = "test_val"
detti_db.set("test_key_2", "test_val_2")
detti_db.set_int("test_int_key", 123)
detti_db.set_float("test_float_key", 123.123)
detti_db.set_list("test_list_key", ["a", 1])

# getters
print("test_key -> {}".format(detti_db["test_key"]))
print("test_int_key -> {}".format(detti_db.get("test_int_key")))
print("test_list_key -> {}".format(detti_db["test_list_key"]))
print("All content: {}".format(detti_db.get_all()))
print("Number of elements in DB: {}".format(detti_db.get_number_of_elements()))
print("Size of DB: {}".format(detti_db.size_of_db()))
print("All keys in DB: {}".format(detti_db.get_all_keys()))

# deletions
del detti_db["test_key"]
detti_db.delete("test_key_2")

# Set some new items for searching
detti_db["test_key_3"] = "my_test_val_3"
detti_db["my_test_key_4"] = "test_val_4"

# Searching
print("'my_' key prefixes -> {}".format(detti_db.search_keys_in_db("my_")))
print("'my_' value prefixes -> {}".format(detti_db.search_values_in_db("my_")))
