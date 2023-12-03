from PyQt5.QtCore import pyqtSignal, QObject

from app.src.backend.integration import Property, TrProperty, PropertyMeta
from app.src.localization import ChainTrText


class PropertyForTests(QObject, metaclass=PropertyMeta):
    prop_signal = pyqtSignal()

    prop1 = Property(42)
    prop2 = Property("default_value", constant=True)
    prop3 = Property([])

    tr_prop1 = TrProperty()
    tr_prop2 = TrProperty("default_text")


def test_property_initialization():
    obj = PropertyForTests()

    assert obj.prop1 == 42
    assert obj.prop2 == "default_value"
    assert obj.prop3 == []
    assert isinstance(obj.tr_prop1, ChainTrText)
