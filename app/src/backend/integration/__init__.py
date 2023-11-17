import copy

from PyQt5.QtCore import pyqtProperty, QObject, pyqtSignal
from app.src.localization import ChainTrText


class Property(pyqtProperty):
    prefix_inst_name_attr = "_property_meta_cls__{}"
    fin_signal_name = '{}Changed'

    def __init__(self, value, constant=False):
        self.default_value = value
        self.constant = constant
        self.name = ""

    def init_by(self, *args, **kwargs):
        super(Property, self).__init__(*args, **kwargs)
        return self

    def setter(self, inst=None, value=None):
        if self.getter(inst) != value:
            setattr(inst, self.prefix_inst_name_attr.format(self.name), value)
            getattr(inst, self.fin_signal_name.format(self.name)).emit(value)

    def getter(self, inst, **kwargs):
        inst_name_attr = self.prefix_inst_name_attr.format(self.name)
        if hasattr(inst, inst_name_attr):
            return getattr(inst, inst_name_attr)

        # for case:
        # Property([...], constant=True)
        if self.constant:
            return self.default_value

        if isinstance(self.default_value, list):
            # for case: Property([])
            list_cpy = copy.deepcopy(self.default_value)
            setattr(inst, inst_name_attr, list_cpy)
            getattr(inst, self.fin_signal_name.format(self.name)).emit(list_cpy)
            return list_cpy

        return self.default_value

    def add_to(self, attrs, key):
        type_ = type(self.default_value)

        kwargs = dict(fget=self.getter)
        if self.constant:
            kwargs.update(constant=True)
        else:
            notifier = pyqtSignal(type_)
            attrs[self.fin_signal_name.format(key)] = notifier
            kwargs.update(fset=self.setter, notify=notifier)
        self.name = key
        attrs[key] = self.init_by(type_, **kwargs)


class TrProperty(Property):
    def __init__(self, value=None, *args, **kwargs):
        super(TrProperty, self).__init__(value, *args, **kwargs)

    def setter(self, inst=None, value=None):
        attr = self.prefix_inst_name_attr.format(self.name)
        if not hasattr(inst, attr):
            setattr(inst, attr, ChainTrText())
        text = getattr(inst, attr)
        text.set_text(value)
        getattr(inst, self.fin_signal_name.format(self.name)).emit(text)

    def getter(self, inst, **kwargs):
        attr = self.prefix_inst_name_attr.format(self.name)
        if hasattr(inst, attr):
            return getattr(inst, attr)
        result = ChainTrText()
        if self.default_value:
            result.set_text(self.default_value)
        setattr(inst, attr, result)
        return result

    def add_to(self, attrs, key):
        self.name = key
        type_ = ChainTrText
        notifier = pyqtSignal(type_)
        attrs[self.fin_signal_name.format(key)] = notifier
        attrs[key] = self.init_by(type_, fget=self.getter, fset=self.setter, notify=notifier)


class PropertyMeta(type(QObject)):
    def __new__(cls, name, bases, attrs):
        for key in list(attrs.keys()):
            attr = attrs[key]
            if not isinstance(attr, Property):
                continue
            attr.add_to(attrs, key)
        return super(PropertyMeta, cls).__new__(cls, name, bases, attrs)
