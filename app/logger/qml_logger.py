from PyQt5.QtCore import QObject, pyqtSlot

from . import logger


class QmlLogger(QObject):
    @pyqtSlot(str)
    def error(self, message):
        logger.error(f"<QML> {message!r}".replace('<', r'\<'))

    @pyqtSlot(str)
    def info(self, message):
        logger.info(f"<QML> {message!r}".replace('<', r'\<'))
