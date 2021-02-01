# Logging

The generated log files will be placed in this folder (`logs`).

The generated log files are skipped in the ".gitignore" file (`logs/*.log`).

Currently, the project uses the own implemented colorized logger.

**You can find the implementation:**
 - tools/color_logger.py

You can set the logging level in the config file with the below parameter:

```ini
# Level of the logger. Possible: DEBUG, INFO, WARNING, ERROR, CRITICAL
# IMPORTANT: The generated log file will contain all log level messages!
log_level = WARNING
```

As it is marked in the default config file, the all log levels are redirected to the generated log file.

## Log file name

All generated log file names are unique. It contains the name of the module, and the current date/time.

**Format of log file name in case of detti DB:**
 - `detti_db_<%Y%m%d_%H%M%S>.log` (Year Month Day Hour Minute Second)

## Log format

The default console log format:
```python
"[$BOLD%(asctime)-20s$RESET][$BOLD%(name)-10s$RESET][%(levelname)-18s] %(message)-80s ($BOLD%(filename)s$RESET:%(lineno)d:%(funcName)s)"
```

The default log file format:
```python
"[%(asctime)-20s][%(name)-20s][%(levelname)-15s] %(message)-100s (%(filename)s:%(lineno)d:%(funcName)s)"
```

You can read about possible formatting:
 - [Logging facility for Python](https://docs.python.org/3/library/logging.html)