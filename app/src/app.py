import asyncio
import errno
import os
import sys
import traceback
from pathlib import Path

from PyQt5.QtCore import QUrl
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtWidgets import QApplication
from qasync import QEventLoop

from app.logger import logger
from app.logger.qml_logger import QmlLogger
from app.src.backend.session import Session
from app.src.localization import Translator


class Application:
    def __init__(self, *args, run_with_errors=True):
        self.app = QApplication([sys.argv[0], *args])
        loop = QEventLoop(self.app)
        asyncio.set_event_loop(loop)
        loop.set_exception_handler(self.exception_handler)
        self.engine = QQmlApplicationEngine()
        self.has_qml_error = False
        self.run_with_errors = run_with_errors
        self.translator = Translator()
        self.translator.signalChangeLang.connect(self.engine.retranslate)
        self.session = Session()
        self.logger = QmlLogger()

    def set_up_root_context(self):
        context = self.engine.rootContext()
        context.setContextProperty("session", self.session)
        context.setContextProperty("logger", self.logger)
        context.setContextProperty("translator", self.translator)

    def init_app(self):
        self.app.setApplicationName('Music app')
        self.app.setApplicationVersion('1.0.0')

        self.translator.install_tr('en')
        self.engine.warnings.connect(self.error_handler)
        self.set_up_root_context()
        self.engine.quit.connect(self.app.quit)

        self.engine.load(QUrl("qrc:/App.qml"))

        objects = self.engine.rootObjects()
        if (self.has_qml_error and not self.run_with_errors) or not objects:
            print('Fail init application :(', self.has_qml_error, len(objects))
            sys.exit(errno.ENODATA)
        main_window = objects[0]
        main_window.showMaximized()

        self.engine.warnings.disconnect(self.error_handler)

    def start_app(self):
        logger.info('App started')
        loop = asyncio.get_event_loop()
        with loop:
            sys.excepthook = self.exception_hook
            code = loop.run_forever()
        self.storage.close_environment()
        self.app.quit()
        logger.info(f'App was closed with code: {code}')
        os._exit(code)

    def exception_handler(self, selector, context):
        exception = context["exception"]
        exc_info = (type(exception), exception, exception.__traceback__)
        self.exception_hook(*exc_info)

    @staticmethod
    def exception_hook(exc_type, error, tb):
        if issubclass(exc_type, KeyboardInterrupt):
            logger.debug(f"Program was interrupted {error}")
            sys.__excepthook__(exc_type, error, tb)
            sys.exit(1)
        message = "".join(traceback.format_tb(tb))
        logger.critical(f"Detect program crash {error!r}:\n{message}")

    def error_handler(self, errors):
        self.has_qml_error = True
        for error in errors:
            logger.error(error.toString().replace('<', r'\<'))

