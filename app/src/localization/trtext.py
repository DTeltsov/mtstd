from PyQt5 import sip
from PyQt5.QtCore import QObject, pyqtSignal, QCoreApplication, pyqtProperty, pyqtSlot
from PyQt5.QtQml import qmlRegisterType


class CurrentLangInfoHolder:
    lang = ''

    @classmethod
    def memorize_lang(cls, lang):
        cls.lang = lang


class Emitter(QObject):
    signalReTranslate = pyqtSignal()
    signalReTranslateLangParam = pyqtSignal(str)


emitter = Emitter()
current_lang_info_holder = CurrentLangInfoHolder()


class AbstractTrText(QObject):
    _memory = {}

    def __init__(self, *args, memorize=False, **kwargs):
        super(AbstractTrText, self).__init__(*args, **kwargs)
        self._text = ''
        if memorize:
            # uses to hold a reference to an object created/passed in qml
            self._memory[id(self)] = self
        self.re_translate()
        emitter.signalReTranslate.connect(self.re_translate)

    textChanged = pyqtSignal(str)

    @pyqtProperty(str, notify=textChanged)
    def text(self):
        return self._text

    def re_translate(self):
        if not sip.isdeleted(self):
            self.textChanged.emit(self._text)

    def deleteLater(self):
        self._memory.pop(id(self), None)
        if not sip.isdeleted(self):
            super(AbstractTrText, self).deleteLater()

    def __str__(self):
        return self._text


class TrText(AbstractTrText):
    def __init__(self, *args, key='', context='', params=None, **kwargs):
        self._key = key
        self._context = context
        if params is None:
            params = []
        self._args = params
        super(TrText, self).__init__(*args, **kwargs)

        self.keyChanged.connect(self.re_translate)
        self.contextChanged.connect(self.re_translate)
        self.argsChanged.connect(self.re_translate)

    def __eq__(self, other):
        if not isinstance(other, TrText):
            return False
        return (self._key, self._context, self._args) == (other._key, other._context, other._args)

    def __hash__(self):
        return hash(f'{self._key} {self._context} {self._args}')

    keyChanged = pyqtSignal()

    @pyqtProperty(str, notify=keyChanged)
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = value
        self.keyChanged.emit()

    contextChanged = pyqtSignal()

    @pyqtProperty(str, notify=contextChanged)
    def context(self):
        return self._context

    @context.setter
    def context(self, value):
        self._context = value
        self.contextChanged.emit()

    argsChanged = pyqtSignal()

    @pyqtProperty(list, notify=argsChanged)
    def args(self):
        return self._args

    @args.setter
    def args(self, value):
        self._args = value
        self.argsChanged.emit()

    def re_translate(self):
        translation = QCoreApplication.translate(self._context, self._key)
        try:
            self._text = translation.format(*self._args)
        except IndexError:
            return
        super(TrText, self).re_translate()

    def __repr__(self):
        return f"<TrText {self._context}.{self._key}{self._args}>"

    def __eq__(self, other):
        if not isinstance(other, TrText):
            return False
        return (self._key == other._key
                and self._context == other._context
                and self._args == other._args)


class DefectTrText(AbstractTrText):
    DEFAULT_LANG = 'en'

    def __init__(self, defect_data: dict = None, name_key: str = '', *args, **kwargs):
        self.translations = dict()
        self.current_lang = current_lang_info_holder.lang
        if defect_data:
            self.set_translates(defect_data, name_key)
        super(DefectTrText, self).__init__(*args, **kwargs)
        emitter.signalReTranslateLangParam.connect(self.re_translate_lang_param)

    def set_translates(self, data: dict, name_key: str):
        for attr in data:
            if name_key == attr:
                self.translations[self.DEFAULT_LANG] = data[attr]
            elif name_key in attr:
                lang = attr.split('_')[-1]
                self.translations[lang] = data[attr]

    def re_translate(self):
        if not sip.isdeleted(self):
            lang = self.current_lang if self.current_lang != 'uk' else 'ua'
            text = self.translations.get(lang) or self.translations.get(self.DEFAULT_LANG) or 'ERROR. Not translated'
            self._text = text
            super(DefectTrText, self).re_translate()

    def re_translate_lang_param(self, lang=None):
        if not sip.isdeleted(self):
            self.current_lang = lang or current_lang_info_holder.lang


class ChainTrText(AbstractTrText):
    def __init__(self, *args, **kwargs):
        self._chain = []
        super(ChainTrText, self).__init__(*args, **kwargs)

    @pyqtSlot(QObject, name='setText')
    @pyqtSlot(str, name='setText')
    def set_text(self, text, *args, **kwargs):
        self.clear()
        chain = text._chain if isinstance(text, ChainTrText) else [text]
        if isinstance(text, ChainTrText):
            text._chain = []
            text.deleteLater()

        self._chain = chain
        self.re_translate()

    def re_translate(self):
        translations = [(
            i.re_translate() or i.text if isinstance(i, AbstractTrText)
            else str(i))
            for i in self._chain
        ]
        self._text = ''.join(translations)
        super(ChainTrText, self).re_translate()

    @pyqtSlot(QObject)
    @pyqtSlot(str)
    def chain(self, other):
        if isinstance(other, ChainTrText):
            self._chain.extend(other._chain)
            other._chain = []
            other.deleteLater()
        else:
            self._chain.append(other)
        self.re_translate()

    @pyqtSlot()
    def clear(self):
        [obj.deleteLater() for obj in self._chain if isinstance(obj, QObject)]
        self._chain.clear()
        self._text = ''
        self.textChanged.emit(self._text)

    def __repr__(self):
        return f"<ChainTrText {'+'.join([repr(i) for i in self._chain])}>"

    def deleteLater(self):
        self.clear()
        super(ChainTrText, self).deleteLater()


qmlRegisterType(TrText, "AQML", 1, 0, 'TrText')
qmlRegisterType(ChainTrText, "AQML", 1, 0, 'ChainTrText')
