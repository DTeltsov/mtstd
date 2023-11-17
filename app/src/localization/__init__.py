import json

from .translator import Translator, translate
from .trtext import AbstractTrText, TrText, ChainTrText, emitter


class TrTextEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, AbstractTrText):
            return obj.text
        return super(TrTextEncoder, self).default(obj)


def pythonize(obj):
    new = json.loads(json.dumps(obj, cls=TrTextEncoder))
    return new
