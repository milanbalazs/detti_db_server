"""
This file contains the all logging related attributes.
Actually it is a colored and configurable logger.
It can handle the following colors:
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE
The inherited child class can handle the following parameters:
    name - Name of the created logger.
    log_file_path - If you want to create a log file, you have to set this parameter.
                    It should be the path of log file.
        Default = None (It you don't set this parameter, log file won't be written.)
    console_level - Set the log level of console output.
        Default = logging.DEBUG
    file_level - Set the log level of log file (It is optional).
        Default = logging.DEBUG
Instance creation example:
    Code part:
        my_logger = ColoredLogger(__file__, log_file_path="test_log.log")
        my_logger.info("Info")
        my_logger.warning("Warning")
        my_logger.error("Error")
    Output:
        [2019-11-25 18:15:37,946][custom_logger.py    ][INFO   ]  Info (custom_logger.py:83)
        [2019-11-25 18:15:37,946][custom_logger.py    ][WARNING]  Warning (custom_logger.py:84)
        [2019-11-25 18:15:37,946][custom_logger.py    ][ERROR  ]  Error (custom_logger.py:85)
"""

from logging import Formatter, Logger, INFO, DEBUG, FileHandler, StreamHandler, addLevelName
from os import mkdir
from os import sep as os_sep
from os.path import isdir, dirname
from os.path import join as path_join
import platform
import errno

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

# The background is set with 40 plus the number of the color, and the foreground with 30

# These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"
addLevelName(31, "OK")


def formatter_message(message, use_color=True):
    """
    Create the colored message.
    :param message: The message which we want to write to console/file.
    :param use_color: The message will be colored if it is True else it won't be colored.
    :return: Formatted message.
    """

    if use_color and "Windows" != platform.system():
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message


COLORS = {
    "WARNING": YELLOW,
    "INFO": WHITE,
    "DEBUG": BLUE,
    "CRITICAL": YELLOW,
    "ERROR": RED,
    "OK": GREEN,
}


class ColoredFormatter(Formatter):
    """
    It is inherited from 'logging.Formatter' class
    and the format method is overwritten is this class.
    This class passed the colored message to "original" logger module.
    """

    def __init__(self, msg, use_color=True):
        """
        Init method of 'ColoredFormatter' class.
        :param msg: The getting message.
        :param use_color: The message will be colored if it is True else it won't be colored.
        """

        Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        """
        Based on the original documentation:
            Format the specified record as text.

            The record's attribute dictionary is used as the operand to a
            string formatting operation which yields the returned string.
            Before formatting the dictionary, a couple of preparatory steps
            are carried out. The message attribute of the record is computed
            using LogRecord.getMessage(). If the formatting string uses the
            time (as determined by a call to usesTime(), formatTime() is
            called to format the event time. If there is exception information,
            it is formatted using formatException() and appended to the message.
        :param record: The record's attribute dictionary is used as the operand to a
            string formatting operation which yields the returned string.
        :return: self
        """

        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        return Formatter.format(self, record)


# Custom logger class with multiple destinations
class ColoredLogger(Logger):
    """
    Own colored logger class.
    It contains the all colored logger related attributes.
    It is inherited from 'logging.Logger' class.
    """

    CONSOLE_FORMAT = (
        "[$BOLD%(asctime)-20s$RESET][$BOLD%(name)-10s$RESET]"
        "[%(levelname)-18s]  %(message)-80s ($BOLD%(filename)s$RESET:%(lineno)d:%(funcName)s)"
    )

    LOG_FILE_FORMAT = (
        "[%(asctime)-20s][%(name)-20s][%(levelname)-15s]  "
        "%(message)-100s (%(filename)s:%(lineno)d:%(funcName)s)"
    )

    COLOR_FORMAT = formatter_message(CONSOLE_FORMAT, True)

    def __init__(self, name, log_file_path=None, console_level=INFO, file_level=DEBUG):
        """
        Init method of 'ColoredLogger' class.
        :param name: Name of logger.
        :param log_file_path: If you want to create a log file, you have to set this parameter.
                              It should be the path of log file.
        :param console_level:  Set the log level of console output.
        :param file_level: Set the log level of log file.
        """

        Logger.__init__(self, name)

        color_formatter = ColoredFormatter(self.COLOR_FORMAT)

        if log_file_path:
            log_folder_path = "{}".format(os_sep).join(log_file_path.split(os_sep)[0:-1])
            if not isdir(log_folder_path):
                try:
                    mkdir(log_folder_path)
                except OSError as exc:
                    if exc.errno != errno.EEXIST:
                        raise exc
                    pass
            # create file handler which logs even debug messages
            log_file_formatter = ColoredFormatter(self.LOG_FILE_FORMAT, use_color=False)
            fh = FileHandler(log_file_path, mode="w")
            fh.setLevel(file_level)
            fh.setFormatter(log_file_formatter)
            self.addHandler(fh)

        console = StreamHandler()
        console.setLevel(console_level)
        console.setFormatter(color_formatter)
        self.addHandler(console)

    def ok(self, message, *args, **kwargs):
        """
        Adding a new colorized OK level to logger.
        :param message: Message on OK level
        :param args: ARGS
        :param kwargs: KWARGS
        :return: None
        """

        if self.isEnabledFor(31):
            self._log(31, message, args, **kwargs)


####
# TEST SECTION
####


if __name__ == "__main__":

    my_logger = ColoredLogger(
        __file__, log_file_path=path_join(dirname(__file__), "logs", "test_log.log")
    )
    my_logger.info("Info")
    my_logger.warning("Warning")
    my_logger.error("Error")
    my_logger.ok("OK")
