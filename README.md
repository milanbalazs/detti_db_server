# detti DB and/or Server
Lightweight Json based key-value DB and/or server.

 - Why:
   - Small, Fast, Easy, Funny

![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+)
**The DB handles only strings as key and value (`Dict[str, str]`).**

## Badges

![PythonBlack](https://github.com/milanbalazs/detti_db/workflows/PythonBlack/badge.svg)
![PythonStyle](https://github.com/milanbalazs/detti_db/workflows/PythonStyle/badge.svg)
![PythonUnitTest](https://github.com/milanbalazs/detti_db/workflows/PythonUnitTest/badge.svg)
## Create an environment

**Create a project folder and a venv folder within:**
```bash
>>> mkdir -p detti
>>> cd detti
>>> python3 -m venv venv
```

**Activation the virtual environment:**
```bash
>>> source venv/bin/activate
```

**Install the required modules from requirements.txt:**
```bash
>>> pip install -r requirements.txt
```

**Clone the source code from Git:**
```bash
>>> git clone https://github.com/milanbalazs/detti_db_server.git
```

**Note:**
 - The PyPi package is in progress (The `pip` can be used in future).

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

### Usage

**Import `DettiDB` class from the `detti_db` module:**

```python
from detti_db import DettiDB
```

**Create instance from `DettiDB` class (Using the default init values):**

```python
detti_db = DettiDB()
```

**Set key-value pair in the detti DB (two possible ways):**

```python
detti_db["test_key"] = "test_val"
detti_db.set("test_key_2", "test_val_2")
```

**Get value of key (two possible ways):**

```python
print(detti_db["test_key"])  # test_val
print(detti_db.get("test_key_2"))  # test_val_2
```

**Get all elements of detti DB (Returning a `Dict[str, str]`):**

```python
print(detti_db.get_all())  # {'test_key': 'test_val', 'test_key_2': 'test_val_2'}
```

**Delete an element from detti DB (two possible ways):**

```python
del detti_db["test_key"]
detti_db.delete("test_key_2")  # Return True if it's success else False
```

**Search keys based on provided prefix (Returning a `Dict[str, str]`):**

```python
print(detti_db.search_keys_in_db("my_"))  # Return eg.: {'my_test_key_4': 'test_val_4'}
```

**Search values based on provided prefix (Returning a `Dict[str, str]`):**

```python
print(detti_db.search_values_in_db("my_"))  # Return eg.: {'test_key_4': 'my_test_val_4'}
```

**Complete example code (With not existing DB):**

```python
from detti_db import DettiDB

detti_db: DettiDB = DettiDB()

detti_db["test_key"] = "test_val"
detti_db.set("test_key_2", "test_val_2")

print(detti_db["test_key"])
print(detti_db.get("test_key_2"))

print(detti_db.get_all())

del detti_db["test_key"]
detti_db.delete("test_key_2")

detti_db["test_key_3"] = "my_test_val_3"
detti_db["my_test_key_4"] = "test_val_4"
print(detti_db.get_all())
print(detti_db.search_keys_in_db("my_"))
print(detti_db.search_values_in_db("my_"))
```

**Output:**

``` bash
>>> python3 test.py
[2021-02-01 12:32:29,368][detti_db.py][INFO   ]  Starting to check the getting config file.                                       (detti_db.py:120:check_config_file)
[2021-02-01 12:32:29,368][detti_db.py][WARNING]  The getting config file's permission is not 600! Recommended to change it. Current permissions: 0o664 (detti_db.py:133:check_config_file)
[2021-02-01 12:32:29,369][detti_db.py][OK     ]  The config file checking has been done!                                          (detti_db.py:136:check_config_file)
[2021-02-01 12:32:29,369][detti_db.py][WARNING]  The '/home/user/detti_db/test.db' DB file doesn't exist.       (detti_db.py:181:load_db)
test_val
test_val_2
{'test_key': 'test_val', 'test_key_2': 'test_val_2'}
{'test_key_3': 'my_test_val_3', 'my_test_key_4': 'test_val_4'}
{'my_test_key_4': 'test_val_4'}
{'test_key_3': 'my_test_val_3'}
```

## detti Server (with RESTful API)

### Configuration

The default config is `detti_conf.ini`.

It is in the root folder (next to the `detti_db.py` file).

The configuration file is a standard [INI file format](https://en.wikipedia.org/wiki/INI_file).

**Default config:**
```ini
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
   sections are related to the Server running. 
   Other sections are not used in case of DB. It is not problem if other 
   (default) sections are not in the config file.

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
### Test server status

The server status can be checked to send a GET request to `/ping` end-point of the server.

Response if the server is up and running:
```bash
>>> curl http://localhost:5000/ping
> "PONG"
```

Response if the server is down (Status code: 7):
```bash
>>> curl http://localhost:5000/ping
> curl: (7) Failed to connect to localhost port 5000: Kapcsolat elutasítva
```

### End-points (RESTful APIs)

**`/get/<string:db_key>`**

Providing the key-value pair based on getting key. The status code is 201 in case of error.

Example:
```bash
>>> curl http://localhost:5000/set -d "exist=value_of_exist_key" -X PUT
> {"STATUS": "OK"}
>>> curl http://localhost:5000/get/exist
> {"exist": "value_of_exist_key"}
>>> curl http://localhost:5000/get/doesnt_exist
> {"doesnt_exist": "The key doesn't exist in DB."}
```
---
**`/set`**

Setting/updating key-value pair in the DB.

Example:
```bash
>>> curl http://localhost:5000/set -d "test_key=test_val" -X PUT
> {"STATUS": "OK"}
>>> curl http://localhost:5000/get/test_key
> {"test_key": "test_val"}
```
---
**`/search_key/<string:key_prefix>`**

Searching keys in the DB based on provided key prefix.

Example:
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
---
**`/search_val/<string:value_prefix>`**

Searching values in the DB based on provided value prefix.

Example:
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
---
**`/delete/<string:db_key>`**

Deleting an element from the DB.

Example:
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

Example:
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

### JWT Authentication

Official page of JWT:
 - [JSON Web Tokens](https://jwt.io)

![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+)
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
 - Creating PyPi package
   - The package can be installed by `pip`
 - Introduce the multithreading/multiprocessing in searching methods
   - In case of big data the multithreading/multiprocessing can reduce the execution time
 - Add support for more data types. 
   - Currently, the value only can be string as well as the key.
   - Adding new supported types in case of value: int, list, dict etc...