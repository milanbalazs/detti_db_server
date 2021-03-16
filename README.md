<p align="center">
  <img src="https://github.com/milanbalazs/detti_db_server/blob/main/doc/pics/detti_db_logo.png?raw=true" alt="detti db server logo"/>
</p>

<h2 align="center">Lightweight Json based key-value DB and/or server.</h2>

<p align="center">
<img src="https://github.com/milanbalazs/detti_db/workflows/PythonBlack/badge.svg">
<img src="https://github.com/milanbalazs/detti_db/workflows/PythonStyle/badge.svg">
<img src="https://github.com/milanbalazs/detti_db/workflows/PythonUnitTest/badge.svg">
<img src="https://github.com/milanbalazs/detti_db_server/workflows/CodeQL/badge.svg">
</p>

<p align="center">
<img src="https://pepy.tech/badge/detti-db-server">
</p>

---

## Introduction

**Why:**
   - Small, Fast, Efficient, Easy, Funny

**Important:**

 - **The Detti DB handles string key, and many value types.**
 - **The Detti Server handles only string type as key and value (`Dict[str, str]`).**

## Links

* [PyPi](https://pypi.org/project/detti-db-server/)
* [GitHub](https://github.com/milanbalazs/detti_db_server)
* [PePy](https://pepy.tech/project/detti-db-server)
* [Example DB usage file](examples/db_example_1.py)
* [Example Server usage file](examples/server_example_1.py)

## Easy install with PIP

```bash
>>> pip install detti-db-server
```

## Create environment and use virtual environment

**Create a project folder and a venv folder within:**
```bash
>>> mkdir -p detti
>>> cd detti
```

**Clone the source code from Git:**
```bash
>>> git clone https://github.com/milanbalazs/detti_db_server.git
>>> cd detti_db_server
```

**Create and activate the virtual environment:**
```bash
>>> python3 -m venv venv
>>> source venv/bin/activate
```

**Install the required modules from requirements.txt:**
```bash
>>> pip install -r requirements.txt
OR
>>> python setup.py install
```

## System

**Requirements:**
 - Interpreter
   - Python3.6.x <
   
 - Python packages
   - They can find in the requirements.txt file ([pipreqs](https://github.com/bndr/pipreqs)).
   - The required packages can be installed with `pip`.

**Tested system:**
 - Interpreter:
   - Python 3.6.9
 - Operation system:
   - Linux Mint 19.1 Tessa
 - Bash:
   - 4.4.20(1)-release
 - Curl
   - curl 7.58.0 (x86_64-pc-linux-gnu)

## detti DB

### Configuration

The default config is `detti_conf.ini`.

It is in the root folder (next to the `detti_db.py` file).

The configuration file is a standard [INI file format](https://en.wikipedia.org/wiki/INI_file).

**Default config:**
```ini
[DETTI_DB]
# Path of the DB file. Recommended to define full path.
path_of_db = test.db
# Maximum length of the keys in DB (Avoid memory overload).
len_of_key = 100
# Maximum length of the values in DB (Avoid memory overload).
len_of_val = 100
# Level of the logger. Possible: DEBUG, INFO, WARNING, ERROR, CRITICAL
# IMPORTANT: The generated log file will contain all log level messages!
log_level = WARNING
```
**Note:**
 - The default `detti_conf.ini` file contains more sections but only the `DETTI_DB` section is 
   related to the DB. Other sections are not used in case of DB. It is not problem if other 
   (default) sections are not in the config file.

**Use own config file:**
 - There is `config_file` argument (`str`) of `DettiDB` class which set the used config file path.
 - Example:
   - ```python
      detti_db = DettiDB(config_file="own_config.ini")
     ```

**Owerwrite config file parameters:**
 - You can overwrite all config file parameters as instance variables.
 - Example:
   - ```python
      detti_db = DettiDB(len_of_val=50)  # The parameter is set to 100 in config file but it will be overwrite to 50.
     ```
### Usage

**Import `DettiDB` class from the `detti_db` module:**

```python
from detti_db import DettiDB
```

**Create instance from `DettiDB` class (Using the default init values):**

```python
detti_db = DettiDB()
```

**Supported types in DB:**

 - Key
   -  `str`
 - Value
   - `str`
   - `float`
   - `int`
   - `list`
   - `dict`

---

:arrow_right: **Setters:**

**Key: `str`, Value: `str`:**

With dictionary like solution:

```python
detti_db["test_str_key"] = "test_val"  # Set the value as "test_val" (str)
```

:Return: `True` if the setting is successful else `False`

Note:
 - If you want to set a non-supported value type, you will get a warning message, and
   the value won't be store to DB. Eg.:
   - ```python
     detti_db["test_key"] = (1, 2, 3)  # Try to store Tuple type
     >> [detti_db.py][WARNING]  The getting value type is not supported (<class 'tuple'>). The value won't be stored.
     ```


With method usage:

```python
detti_db.set("test_str_key_2", "test_val_2")  # Set the value as "test_val_2" (str)
```

:Return: `True` if the setting is successful else `False`

Note:
 - The `set()` method tries to cast the getting value to string. Eg.:
 - ```python
   detti_db.set("test_str_key_3", 123)  # Set the value as "123" (str)
   ```
   
---

**Key: `str`, Value: `int`:**

With dictionary like solution:

```python
detti_db["test_int_key"] = 8  # Set the value as 8 (int)
```

:Return: `True` if the setting is successful else `False`

With method usage:

```python
detti_db.set_int("test_int_key_2", 9)  # Set the value as 9 (int)
```

:Return: `True` if the setting is successful else `False`

Note:
 - The `set_int()` method tries to cast the getting value to integer. Eg.:
 - ```python
   detti_db.set_int("test_int_key_3", 123.123)  # Set the value as 123 (int)
   detti_db.set_int("test_int_key_4", "888")  # Set the value as 888 (int)
   ```

---

**Key: `str`, Value: `float`:**

With dictionary like solution:

```python
detti_db["test_float_key"] = 8.8  # Set the value as 8.8 (float)
```

:Return: `True` if the setting is successful else `False`

With method usage:

```python
detti_db.set_float("test_float_key_2", 9.9)  # Set the value as 9.9 (float)
```

:Return: `True` if the setting is successful else `False`

Note:
 - The `set_float()` method tries to cast the getting value to float. Eg.:
 - ```python
   detti_db.set_float("test_float_key_3", 123)  # Set the value as 123.0 (float)
   detti_db.set_float("test_float_key_4", "888.888")  # Set the value as 888.888 (float)
   ```

---

**Key: `str`, Value: `List[Any]`:**

With dictionary like solution:

```python
detti_db["test_list_key"] = ["a", 1]  # Set the value as ["a", 1] (list)
```

:Return: `True` if the setting is successful else `False`

With method usage:

```python
detti_db.set_list("test_list_key_2", ["a", 1])  # Set the value as ["a", 1] (list)
```

:Return: `True` if the setting is successful else `False`

Note:
 - The `set_list()` method tries to cast the getting value to float. Eg.:
 - ```python
   detti_db.set_list("test_list_key_3", ("a", 2))  # Set the value as ["a", 2] (list)
   detti_db.set_list("test_list_key_4", "abc")  # Set the value as ["a", "b", "c"] (list))
   ```

---

**Append `Any` to `list`:**

```python
detti_db.append_list("key", "value")
```

Example:
```python
detti_db.set_list("test_list", ["a", 1])
detti_db.append_list("test_list", 666)
print(detti_db["test_list"])
>>> ["a", 1, 666]
```

:Return: `True` if the appending is successful else `False`

Note:
 - The return value is `False` if you try to append a new element to a not existing key in DB.
 - The return value is `False` if you try to append a new element to a key which value is not list type.

---

**Key: `str`, Value: `dict`:**

With dictionary like solution:

```python
detti_db["test_dict_key"] = {"a": 1}  # Set the value as {"a": 1} (dict)
```

:Return: `True` if the setting is successful else `False`

With method usage:

```python
detti_db.set_dict("test_dict_key_2", {"a": 1})  # Set the value as {"a": 1} (dict)
```

---

:arrow_right: **Getters:**

**Get element**

With dictionary like solution:

```python
detti_db["test_key"]  # Return: "test_val"
```

:Return: The requested value if it exists in DB else `None`

With method usage:

```python
detti_db.get("test_key_2")  # Return: "test_val_2"
```

:Return: The requested value if it exists in DB else `None`

Note:
 - The above getter solutions can return any types.

Using default value in get:

```python
detti_db.get("not_exist_key", default_value=5)  # Return: 5 (Due to the "not_exist_key" key is not in DB.)
```

:Return: The requested value if it exists in DB else the set default value.

Note:
 - The above getter solutions can return any types.
 - Any type can be set as default parameter.

---

**Get all elements:**

The `get_all()` method provides the all key-value pairs from DB in Json format. It supports any types.

```python
detti_db.get_all()  # Return: {'test_key': 'test_val', 'test_key_2': 'test_val_2'}
```

:Return: The requested items in dict if any exists in DB else empty dict

---

**Check if key exists in DB:**

The `is_exist()` method returns `True` if the key is in DB else `False`.

```python
detti_db.is_exist("elem_key")
```

:Return: `True` if the key is in DB else `False`.

---

**Deletion:**

With dictionary like solution:

```python
del detti_db["test_key"]
```

:Return: `True` if the setting is successful else `False`

With method usage:

```python
detti_db.delete("test_key_2")  # Return True if it's success else False
```

:Return: `True` if the setting is successful else `False`

---

**Searching:**

**Search keys based on provided prefix (Returning a `Dict[str, str]`):**

```python
detti_db.search_keys_in_db("my_")  # Return: {'my_test_key_4': 'test_val_4'}
```

:Return: The requested items in dict if any exists in DB else empty dict

---

**Search values based on provided prefix (Returning a `Dict[str, str]`):**

```python
detti_db.search_values_in_db("my_")  # Return: {'test_key_4': 'my_test_val_4'}
```

:Return: The requested items in dict if any exists in DB else empty dict

---

**Get size of DB:**

```python
detti_db.size_of_db()  # Return: 666 (int)
```

:Return: Size of the DB is bytes (`int`).

---

**Get all keys of DB:**

```python
detti_db.get_all_keys()  # Return: ["test_key", "test"key_2"] (List[str])
```

:Return: All keys of the DB (`List[str]`).

---

**Dump the current loaded DB to Json file:**

```python
detti_db.dump_to_json("dump.json")
```

Possible parameters:
 - `file_path`: Path of the destination file.
 - `force`: If it is given the existing file will be overwritten.
   - Default: False
 - `permissions`: Set the permission of file. It is true for overwritten files! Octal!
   - Default: 0o600

Eg.:
```python
detti_db.dump_to_json(file_path="dump.json", force=True, permissions=0o664)
```

---

**Complete example code (With not existing DB):**

```python
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
detti_db.set_dict("test_dict_key", {"b": 2})

# getters
print("test_key -> {}".format(detti_db["test_key"]))
print("test_int_key -> {}".format(detti_db.get("test_int_key")))
print("test_list_key -> {}".format(detti_db["test_list_key"]))
print("test_dict_key -> {}".format(detti_db["test_dict_key"]))
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
```

**Output:**

``` bash
>>> python3 examples/db_example_1.py
test_key -> test_val
test_int_key -> 123
test_list_key -> ['a', 1]
test_dict_key -> {'b': 2}
All content: {'test_key': 'test_val', 'test_key_2': 'test_val_2', 'test_int_key': 123, 'test_float_key': 123.123, 'test_list_key': ['a', 1], 'test_dict_key': {'b': 2}}
Number of elements in DB: 6
Size of DB: 216
All keys in DB: ['test_key', 'test_key_2', 'test_int_key', 'test_float_key', 'test_list_key', 'test_dict_key']
'my_' key prefixes -> {'my_test_key_4': 'test_val_4'}
'my_' value prefixes -> {'test_key_3': 'my_test_val_3'}

```

## detti Server (with RESTful API)

### Configuration

The default config is `detti_conf.ini`.

It is in the root folder (next to the `detti_db.py` file).

The configuration file is a standard [INI file format](https://en.wikipedia.org/wiki/INI_file).

**Default config:**
```ini
[DETTI_DB]
# Path of the DB file. Recommended to define full path.
path_of_db = test.db
# Maximum length of the keys in DB (Avoid memory overload).
len_of_key = 100
# Maximum length of the values in DB (Avoid memory overload).
len_of_val = 100
# Level of the logger. Possible: DEBUG, INFO, WARNING, ERROR, CRITICAL
# IMPORTANT: The generated log file will contain all log level messages!
log_level = WARNING

[SERVER]
host = localhost
port = 5000
debug = True
# Setting the request limits in different unites. The most strict will be used!
sec_limit = 5
min_limit = 300
hour_limit = 18000
day_limit = 432000
# IMPORTANT
# If you set the user and password parameter the DB will be accessed with JWT Token!
user =
password =
```
**Note:**
 - The default `detti_conf.ini` file contains more sections but the `SERVER` and `DETTI_DB` 
   sections are related (and mandatory) to the Server running. 
   Other sections are not used in case of DB. It is not problem if other 
   (default) sections are not in the config file.

**Use own config file:**
 - There is `config_file` CLI argument (`str`).
   - Force to use a config file. Default: `detti_conf.ini` (In root folder)
 - Example:
   - `>>> python3 detti_server --config_file my_own_config.ini`

### Usage

**Start the server:**

```bash
>>> python3 detti_server.py
```

**Output in case of successful starting (with the default config):**

```
 * Serving Flask app "detti_server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://localhost:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 217-599-780

```
---

### Test server status

The server status can be checked to send a GET request to `/ping` end-point of the server.

Response if the server is up and running:

Curl:
```bash
>>> curl http://localhost:5000/ping
> "PONG"
```

Python:
```python
import requests
requests.get("http://localhost:5000/ping")  # Return: "PONG"
```

Response if the server is down (Status code: 7):
```bash
>>> curl http://localhost:5000/ping
> curl: (7) Failed to connect to localhost port 5000: Kapcsolat elutasítva
```

---

### End-points (RESTful APIs)

**`/get/<string:db_key>`**

Providing the key-value pair based on getting key. The status code is 201 in case of error.

Curl:
```bash
>>> curl http://localhost:5000/set -d "exist=value_of_exist_key" -X PUT
> {"STATUS": "OK"}
>>> curl http://localhost:5000/get/exist
> {"exist": "value_of_exist_key"}
>>> curl http://localhost:5000/get/doesnt_exist
> {"doesnt_exist": "The key doesn't exist in DB."}
```

Python:
```python
import requests

# Set an element in the DB
put_resp = requests.put("http://localhost:5000/set", data={"exist": "value_of_exist_key"})
print(put_resp.json())  # Return: {"STATUS": "OK"}

# Get the element from DB
resp = requests.get("http://localhost:5000/get/exist")
print(resp.json())  # Return: {"exist": "value_of_exist_key"}
```
---

**`/set`**

Setting/updating key-value pair in the DB.

Curl:
```bash
>>> curl http://localhost:5000/set -d "test_key=test_val" -X PUT
> {"STATUS": "OK"}
>>> curl http://localhost:5000/get/test_key
> {"test_key": "test_val"}
```

Python:
```python
import requests

# Set an element in the DB
put_resp = requests.put("http://localhost:5000/set", data={"test_key": "test_val"})
print(put_resp.json())  # Return: {"STATUS": "OK"}

# Get the element from DB
resp = requests.get("http://localhost:5000/get/test_key")
print(resp.json())  # Return: {"test_key": "test_val"}
```

---

**`/search_key/<string:key_prefix>`**

Searching keys in the DB based on provided key prefix.

Curl:
```bash
>>> curl http://localhost:5000/set -d "test_key=test_val" -X PUT
>  {"STATUS": "OK"}
>>> curl http://localhost:5000/set -d "prod_key_1=prod_val_1" -X PUT
>  {"STATUS": "OK"}
>>> curl http://localhost:5000/set -d "prod_key_2=prod_val_2" -X PUT
>  {"STATUS": "OK"}
>>> curl http://localhost:5000/search_key/prod_
> {
        "prod_key_1": "prod_val_1",
        "prod_key_2": "prod_val_2"
  }
>>> curl http://localhost:5000/search_key/not_exist
>  {"not_exist": "Cannot find keys for prefix"}
```

Python:
```python
import requests

# Set some elements in DB.
requests.put("http://localhost:5000/set", data={"dev_data": "dev"})
requests.put("http://localhost:5000/set", data={"prod_key_1": "prod_val_1"})
requests.put("http://localhost:5000/set", data={"prod_key_2": "prod_val_2"})

# Get the elements based on provided KEY prefix.
resp = requests.get("http://localhost:5000/search_key/prod_")
print(resp.json())  # Return: {"prod_key_1": "prod_val_1", "prod_key_2": "prod_val_2"}

# Try a KEY prefix which is not contained in keys.
resp = requests.get("http://localhost:5000/search_key/nonono")
print(resp.json())  # Return: {"nonono": "Cannot find keys for prefix"}
```

---

**`/search_val/<string:value_prefix>`**

Searching values in the DB based on provided value prefix.

Curl:
```bash
>>> curl http://localhost:5000/set -d "test_key=test_val" -X PUT
>  {"STATUS": "OK"}
>>> curl http://localhost:5000/set -d "prod_key_1=prod_val_1" -X PUT
>  {"STATUS": "OK"}
>>> curl http://localhost:5000/set -d "prod_key_2=prod_val_2" -X PUT
>  {"STATUS": "OK"}
>>> curl http://localhost:5000/search_val/prod_
> {
        "prod_key_1": "prod_val_1",
        "prod_key_2": "prod_val_2"
  }
>>> curl http://localhost:5000/search_val/not_exist
> {"not_exist": "Cannot find values for prefix"}
```

Python:
```python
import requests

# Set some elements in DB.
requests.put("http://localhost:5000/set", data={"dev_data": "dev"})
requests.put("http://localhost:5000/set", data={"prod_key_1": "prod_val_1"})
requests.put("http://localhost:5000/set", data={"prod_key_2": "prod_val_2"})

# Get the elements based on provided VALUE prefix.
resp = requests.get("http://localhost:5000/search_val/prod_")
print(resp.json())  # Return: {"prod_key_1": "prod_val_1", "prod_key_2": "prod_val_2"}

# Try a VALUE prefix which is not contained in keys.
resp = requests.get("http://localhost:5000/search_val/nonono")
print(resp.json())  # Return: {"nonono": "Cannot find values for prefix"}
```

---

**`/delete/<string:db_key>`**

Deleting an element from the DB.

Curl:
```bash
>> curl http://localhost:5000/set -d "test_key=test_val" -X PUT
> {"STATUS": "OK"}
>> curl http://localhost:5000/get/test_key
> {"test_key": "test_val"}
>> curl http://localhost:5000/delete/test_key -X DELETE
> {"STATUS": "OK"}
>> curl http://localhost:5000/get/test_key
> {"test_key": "The key doesn't exist in DB."}
```

Python:
```python
import requests

# Set some elements in DB.
requests.put("http://localhost:5000/set", data={"to_be_deleted": "dummy"})

# Delete the created item
del_resp = requests.delete("http://localhost:5000/delete/to_be_deleted")
print(del_resp.json())  # Return: {"STATUS": "OK"}

# Try to get the deleted item
resp = requests.get("http://localhost:5000/get/to_be_deleted")
print(resp.status_code)  # Return: 201
print(resp.json())  # Return: {"to_be_deleted": "The key doesn't exist in DB."}
```

---

**`/ping`**

Checking if the server is running.

Success example:
```bash
>>> curl http://localhost:5000/ping
> "PONG"
```

Failed example (Status code: 7):
```bash
>>> curl http://localhost:5000/ping
> curl: (7) Failed to connect to localhost port 5000: Kapcsolat elutasítva
```

---

**`/getall`**

Providing all elements from the DB. {key: value, key: value}

Curl:
```bash
>>> curl http://localhost:5000/set -d "test_key=test_val" -X PUT
> {"STATUS": "OK"}
>>> curl http://localhost:5000/set -d "test_key_1=test_val_1" -X PUT
> {"STATUS": "OK"}
>>> curl http://localhost:5000/getall
> {
        "test_key": "test_val",
        "test_key_1": "test_val_1"
  }
```

Python:
```python
import requests

# Set some elements in DB.
requests.put("http://localhost:5000/set", data={"get_all_1": "dummy"})
requests.put("http://localhost:5000/set", data={"get_all_2": "dummy"})

# Getting all elements from DB.
resp = requests.get("http://localhost:5000/getall")
print(resp.json()) # Return: {"get_all_1": "dummy", "get_all_2": "dummy"}
```

### JWT Authentication

Official page of JWT:
 - [JSON Web Tokens](https://jwt.io)

**Important:**
 - The JWT authentication is not active with the default configuration.

The "user" and "password" parameters have to be set in the configuration file
to activate the JWT Authentication.

**For example:**
```ini
user = test_user
password = test_password
```

**Get the token from the server:**
```bash
>>> curl -i -X POST -H "Content-Type: application/json" -d '{"username":"test_user","password":"test_password"}' http://localhost:5000/auth
> {
      "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTE4...
  }
```

**Use the JWT authentication for APIs:**
```bash
>>> curl -H "Authorization: jwt eyJ0eXAiOiJKV..." http://localhost:5000/get/exist
> {
      "exist": "exist_val"
  }
```

**If the token is not used, the APIs provide error message with 401 status code:**
```bash
>>> curl http://localhost:5000/get/exist
> {
      "description": "Request does not contain an access token",
      "error": "Authorization Required",
      "status_code": 401
  }
```

## Production line

Currently, the production line support is not implemented in this repo (But it is in the road-map)!
You can run the server on the production line with Nginx and Gunicorn.

**Tutorial:**
 - [How To Serve Flask Applications with Gunicorn and Nginx on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04)

## Future
 - Introduce the multithreading/multiprocessing in searching methods
   - In case of big data the multithreading/multiprocessing can reduce the execution time
 - Add support for more data types on server side.

## Change log

### 1.2.1
 - Pass the `**options` parameter in `run_server()` function.
   - The options to be forwarded to the underlying Werkzeug server.
     See :func:`werkzeug.serving.run_simple` for more information.
 - Add the `dump_to_json()` method to dump the current DB to Json file.
 - Add `Python Black` and `Flake8` pre-commit hooks to repo for better contributions.
 - Fix TypeError in case of `dict` type setting.
 - Add Cross Origin Resource Sharing (CORS) for server to make cross-origin AJAX possible.

### 1.1.1
 - Add `get_number_of_elements()` method to get number of elements of DB.
 - Add `get_all_keys()` method to get all keys of DB.
 - Add `set_dict()` method as `dict` type setter.
 - Add `run_server()` function to server part for better integration.
   - Now the `detti_server.py` file can be imported and configurable before starting the server.
   - Eg.: `import detti_server; detti_server.run_server()`

### 1.1.0
 - Get size of DB with `size_of_db()` method.
 - Implement `__contains__` magic method (Eg.: `"a" in detti_db`).
 - Add `default_value` option to `get` method (Eg.: `detti_db.get("not_exist_key", default_value=5)`)
 - All parameters from config file can be overwritten as `__init__` argument (Eg.: `detti_db = DettiDB(len_of_val=50)`)