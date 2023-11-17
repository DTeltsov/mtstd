import functools
import logging
import os
import pathlib
import queue
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler, QueueHandler

from PyQt5 import QtCore
from loguru import logger, _colorizer

logging_start = datetime.now().strftime('%y-%m-%d_%H:%M:%S')


def colorize_wrapper(func):
    """fix problem with unknown tags in message"""

    @functools.wraps(func)
    def _wrap(string, *args, **kwargs):
        try:
            return func(string, *args, **kwargs)
        except ValueError:
            return func(string.replace('<', r'\<'), *args, **kwargs)

    return _wrap


_colorizer.Colorizer.prepare_simple_message = colorize_wrapper(_colorizer.Colorizer.prepare_simple_message)


def compile_log_file_name() -> str:
    return f"{logging_start}.log"


LEVEL = logging.DEBUG
fmt = "<yellow>{time:%y-%m-%d %H:%M:%S.%f}</> | <level>{level:^7}</level> | " \
      "<cyan>{module:>15} | {function:<20}:{line:<4}</>: <level>{message} </>"
log_file_name = compile_log_file_name()
logs_folder = pathlib.Path('logs').resolve()
path_log = os.path.join(logs_folder, log_file_name)
os.makedirs(logs_folder, 0o777, exist_ok=True)

que = queue.Queue(800)
config = {
    "handlers": [
        {
            "sink": sys.stdout,
            "colorize": True,
            "format": fmt,
        },
        {
            "sink": RotatingFileHandler(
                path_log,
                maxBytes=30 * 1024 * 1024,
                mode='a', backupCount=1,
                encoding="utf8"
            ),
            "backtrace": True,
            "format": fmt
        },
        {
            "sink": QueueHandler(que),
        }
    ],
}
logger.configure(**config)
logger = logger.opt(colors=True)


def qt_log_handler(msg_type: QtCore.QtMsgType, context, message: str):
    path = str(context.file).split('/ui/', 1)[-1]
    if message.startswith('file:'):
        message = message.split(maxsplit=1)[-1]
    if msg_type in [QtCore.QtCriticalMsg, QtCore.QtWarningMsg, QtCore.QtFatalMsg]:
        log = logger.error
    else:
        log = logger.info
    message = message.replace('<', r'\<')
    log(f'QML:{path}:{context.line} `{message}`')


def install_qml_handler():
    QtCore.qInstallMessageHandler(qt_log_handler)
