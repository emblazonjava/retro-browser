import doctest
import importlib

doctest.testmod(importlib.import_module('retrobrowser.framework.builder'))
doctest.testmod(importlib.import_module('retrobrowser.framework.flash'))
doctest.testmod(importlib.import_module('retrobrowser.framework.inputparser'))
doctest.testmod(importlib.import_module('retrobrowser.framework.retrobrowser'))
doctest.testmod(importlib.import_module('retrobrowser.framework.view'))
