import copy

from PyQt5.QtCore import pyqtProperty, QObject, pyqtSignal

from app.src.localization import ChainTrText


class Property(pyqtProperty):
    """
    Custom property class that extends PyQt's pyqtProperty.

    Attributes:
    - default_value: The default value of the property.
    - constant (bool): Indicates whether the property is constant.
    - name (str): The name of the property.

    Methods:
    - __init__(value, constant=False): Initializes a new Property instance.
    - init_by(*args, **kwargs): Initializes the property with additional arguments and keyword arguments.
    - setter(inst=None, value=None): Sets the value of the property and emits the corresponding signal.
    - getter(inst, **kwargs): Gets the value of the property or initializes it if not set.
    - add_to(attrs, key): Adds the property to the given attributes dictionary.

    Note: This class should be used as a decorator for class attributes.
    """
    prefix_inst_name_attr = "_property_meta_cls__{}"
    fin_signal_name = '{}Changed'

    def __init__(self, value, constant=False):
        """
        Initializes a new Property instance.

        Parameters:
        - value: The default value of the property.
        - constant (bool): Indicates whether the property is constant.
        """
        self.default_value = value
        self.constant = constant
        self.name = ""

    def init_by(self, *args, **kwargs):
        """
        Initializes the property with additional arguments and keyword arguments.

        Returns:
        Property: The initialized Property instance.
        """
        super(Property, self).__init__(*args, **kwargs)
        return self

    def setter(self, inst=None, value=None):
        """
        Sets the value of the property and emits the corresponding signal.

        Parameters:
        - inst: The instance of the class.
        - value: The new value of the property.

        Returns:
        None
        """
        if self.getter(inst) != value:
            setattr(inst, self.prefix_inst_name_attr.format(self.name), value)
            getattr(inst, self.fin_signal_name.format(self.name)).emit(value)

    def getter(self, inst, **kwargs):
        """
        Gets the value of the property or initializes it if not set.

        Parameters:
        - inst: The instance of the class.

        Returns:
        Any: The value of the property.
        """
        inst_name_attr = self.prefix_inst_name_attr.format(self.name)
        if hasattr(inst, inst_name_attr):
            return getattr(inst, inst_name_attr)

        if self.constant:
            return self.default_value

        if isinstance(self.default_value, list):
            list_cpy = copy.deepcopy(self.default_value)
            setattr(inst, inst_name_attr, list_cpy)
            getattr(inst, self.fin_signal_name.format(self.name)).emit(list_cpy)
            return list_cpy

        return self.default_value

    def add_to(self, attrs, key):
        """
        Adds the property to the given attributes dictionary.

        Parameters:
        - attrs (dict): The dictionary of class attributes.
        - key (str): The key associated with the property.

        Returns:
        None
        """
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
    """
    Custom property class that extends the Property class and adds translation support.

    Methods:
    - __init__(value=None, *args, **kwargs): Initializes a new TrProperty instance.
    - setter(inst=None, value=None): Sets the value of the property and emits the corresponding signal with translation.
    - getter(inst, **kwargs): Gets the value of the property or initializes it with translation if not set.
    - add_to(attrs, key): Adds the property to the given attributes dictionary with translation support.
    """
    def __init__(self, value=None, *args, **kwargs):
        """
        Initializes a new TrProperty instance.

        Parameters:
        - value: The default value of the property.
        - args, kwargs: Additional arguments and keyword arguments.
        """
        super(TrProperty, self).__init__(value, *args, **kwargs)

    def setter(self, inst=None, value=None):
        """
        Sets the value of the property and emits the corresponding signal with translation.

        Parameters:
        - inst: The instance of the class.
        - value: The new value of the property.

        Returns:
        None
        """
        attr = self.prefix_inst_name_attr.format(self.name)
        if not hasattr(inst, attr):
            setattr(inst, attr, ChainTrText())
        text = getattr(inst, attr)
        text.set_text(value)
        getattr(inst, self.fin_signal_name.format(self.name)).emit(text)

    def getter(self, inst, **kwargs):
        """
        Gets the value of the property or initializes it with translation if not set.

        Parameters:
        - inst: The instance of the class.

        Returns:
        ChainTrText: The value of the property with translation support.
        """
        attr = self.prefix_inst_name_attr.format(self.name)
        if hasattr(inst, attr):
            return getattr(inst, attr)
        result = ChainTrText()
        if self.default_value:
            result.set_text(self.default_value)
        setattr(inst, attr, result)
        return result

    def add_to(self, attrs, key):
        """
        Adds the property to the given attributes dictionary with translation support.

        Parameters:
        - attrs (dict): The dictionary of class attributes.
        - key (str): The key associated with the property.

        Returns:
        None
        """
        self.name = key
        type_ = ChainTrText
        notifier = pyqtSignal(type_)
        attrs[self.fin_signal_name.format(key)] = notifier
        attrs[key] = self.init_by(type_, fget=self.getter, fset=self.setter, notify=notifier)


class PropertyMeta(type(QObject)):
    """
    Metaclass for the QObject-derived class with Property attributes.

    Methods:
    - __new__(cls, name, bases, attrs): Creates a new instance of the class with Property attributes.
    """
    def __new__(cls, name, bases, attrs):
        """
        Creates a new instance of the class with Property attributes.

        Parameters:
        - cls: The metaclass.
        - name (str): The name of the class.
        - bases: The base classes.
        - attrs (dict): The dictionary of class attributes.

        Returns:
        QObject: The new instance of the class with Property attributes.
        """
        for key in list(attrs.keys()):
            attr = attrs[key]
            if not isinstance(attr, Property):
                continue
            attr.add_to(attrs, key)
        return super(PropertyMeta, cls).__new__(cls, name, bases, attrs)
