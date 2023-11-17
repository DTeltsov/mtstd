from .app import Application
try:
    from .resources import *
except ImportError:
    # print("Use pyrcc5 to generate src/resources.py from resources.qrc")
    pass
