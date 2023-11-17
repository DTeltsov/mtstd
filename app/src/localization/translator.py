import typing
from pathlib import Path

from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot, QTranslator, \
    QAbstractListModel, Qt, QModelIndex, QVariant, QSettings, QCoreApplication
from PyQt5.QtWidgets import QApplication

from app.logger import logger
from .trtext import TrText, emitter, current_lang_info_holder

languages = {
    'en': 'English',
    'uk': 'Українська',
}

FOLDER = "translates"


class ListModelLanguages(QAbstractListModel):
    code = Qt.UserRole + 1
    label = Qt.UserRole + 2
    modelData = Qt.UserRole + 3

    def __init__(self):
        super(ListModelLanguages, self).__init__()
        self.languages = languages
        self._data = list(self.languages.items())

    def __getitem__(self, index: int):
        try:
            return self._data[index]
        except IndexError:
            return None

    def roleNames(self) -> typing.Dict[int, bytes]:
        return {
            self.code: b"code",
            self.label: b"label",
            self.modelData: b"modelData",
        }

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data)

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        data = self[index.row()]
        if not data:
            return QVariant()

        if role == self.code:
            return data[0]
        if role == self.label:
            return data[1]
        if role == self.modelData:
            return data[1]
        return data


class Translator(QTranslator):
    TRANSLATION_KEY = "application_language"
    QRC_TEMPLATE_PATH = f":/{FOLDER}/" + "{}.qm"

    langs: ListModelLanguages
    lang: str
    label: str

    def __init__(self):
        super(Translator, self).__init__()
        self.counter = 0
        self._lang = ''
        self._label = ''
        self._langs = ListModelLanguages()
        QApplication.instance().installTranslator(self)
        self.signalChangeLang.connect(lambda: emitter.signalReTranslateLangParam.emit(self.lang))
        self.signalChangeLang.connect(emitter.signalReTranslate)

    @pyqtProperty(QAbstractListModel, constant=True)
    def langs(self):
        return self._langs

    signalChangeLang = pyqtSignal()

    @pyqtProperty(str, notify=signalChangeLang)
    def lang(self):
        return self._lang

    @pyqtProperty(str, notify=signalChangeLang)
    def label(self):
        return self._label or r'¯\_(ツ)_/¯'

    @pyqtSlot(name='installTr')
    @pyqtSlot(str, name='installTr')
    def install_tr(self, lang: str = None):
        q_settings = QSettings()
        self.counter += 1
        if isinstance(lang, str):
            lang = lang.lower()
        if not lang or lang not in self.langs.languages:
            lang = q_settings.value(self.TRANSLATION_KEY, defaultValue='en')
        lang_label = self.langs.languages.get(lang, "")
        logger.info(f"Selected translation language: {lang} ({lang_label}), {self.counter}")
        if self.QRC_TEMPLATE_PATH:
            path = self.QRC_TEMPLATE_PATH.format(lang)
        else:
            path = Path(__file__).parent / FOLDER / f'{lang}.qm'

        loaded = self.load(str(path))
        if not loaded:
            logger.error(f"Translation fails for language: {lang}")
        else:
            q_settings.setValue(self.TRANSLATION_KEY, lang)
            q_settings.sync()

        self._lang = lang
        self._label = lang_label
        current_lang_info_holder.memorize_lang(lang)
        self.signalChangeLang.emit()

    @pyqtSlot(str, list, result=str, name='pyFormat')
    def py_format(self, source: str, args: list):
        return source.format(*args)

    @pyqtSlot("QVariantMap", name="createTranslation", result=TrText)
    def create_translation(self, kwargs: dict):
        return TrText(**kwargs, memorize=True)


def translate(context, text, *args):
    translation = QCoreApplication.translate(context, text, *args)
    return translation
