# detti DB and/or Server
Lightweight Json based key-value DB and/or server.

## Badges

![PythonBlack](https://github.com/milanbalazs/detti_db/workflows/PythonBlack/badge.svg)
![PythonStyle](https://github.com/milanbalazs/detti_db/workflows/PythonStyle/badge.svg)

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
path_of_db = /home/milanbalazs/Asztal/GIT/detti_db/test.db
# Maximum length of the keys in DB (Avoid memory overload).
len_of_key = 100
# Maximum length of the values in DB (Avoid memory overload).
len_of_val = 100
# Level of the logger. Possible: DEBUG, INFO, WARNING, ERROR, CRITICAL
# IMPORTANT: The generated log file will contain all log level messages!
log_level = WARNING
```
**Note:**
 - The default `detti_conf.ini` file contains more section bot only the `DETTI_DB` section is 
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
test_val
test_val_2
{'test_key_3': 'my_test_val_3', 'my_test_key_4': 'test_val_4', 'test_key': 'test_val', 'test_key_2': 'test_val_2'}
{'test_key_3': 'my_test_val_3', 'my_test_key_4': 'test_val_4'}
{'my_test_key_4': 'test_val_4'}
{'test_key_3': 'my_test_val_3'}

```

## detti Server

### Configuration
### Start

## Future