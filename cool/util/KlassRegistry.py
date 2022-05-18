_allKlasses = {}


def getKlassByString(name: str):
    return _allKlasses[name]


def setKlassByString(name: str, content):
    _allKlasses[name] = content


def klassRepeats(klass: str):
    return klass in _allKlasses


def getAllKlasses():
    return _allKlasses


def clearKlassTree():
    _allKlasses.clear()


def getKlass(classname):
    # FIXME It shouldn't return none...
    return _allKlasses.get(classname, None)
