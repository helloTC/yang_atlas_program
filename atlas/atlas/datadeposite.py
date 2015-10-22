import sys
import types

class DataDeposite(object):
    _attrs = []
    _nodump_attrs = []

    def __init__(self, **entries):
        self.__dict__.update(entries)
        for key in (self._attrs + self._nodump_attrs):
            if key not in self.__dict__:
                self.__dict__.update({key:None})

    def __getstate__(self):
        odict = self.__dict__.copy()
        for key in odict.keys():
            if key not in self._attrs:
                del odict[key]
        return odict 

    def __repr__(self):
        args = [ '%s=%s' % (k, vars(self).get(k)) for k in self._attrs + self._nodump_attrs]
        return 'DataDeposite(%s)' % ', '.join(args)


class DataDepositeTk(object):
    def __init__(self, depo=None, depocls=None, *args, **kargs):
        if depo is not None:
            self.depo = depo
        else:
            self.depo = depocls(*args, **kargs)

    def getdepo(self):
        return self.depo
    
    def setdepo(self, depo):
        self.depo = depo

    def deposite(self, value, name, cache=True):
        if cache:
            setattr(self.depo, name, value)
        
    def clear_nodump(self):
        for key in self.depo._nodump_attrs:
            if key in self.depo.__dict__:
                del self.depo.__dict__[key]


class DataDepositeDecorator(DataDepositeTk):
    def add_attr(self, name, value):
        setattr(self.depo, name, value)

    def __dir__(self):
        return self.__dict__.keys() + self.depo.__dict__.keys()

    def __getattr__(self, key):
        if hasattr(self.depo, key):
            return getattr(self.depo, key)
        else:
            raise AttributeError, key


def DataTypedef(cls, attrs):
    return type(cls, (DataDeposite,), {'_attrs':attrs})


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __repr__(self):
        args = [ '%s=%s' % (k, repr(v)) for (k,v) in vars(self).items()]
        return 'Struct(%s)' % ', '.join(args)

def dump_struct_to_main(struct):
    sys.modules['__main__'].__dict__.update(struct.__dict__)

def update(x, **entries):
    if type(x) == types.DictType:
        x.update(entries)
    else:
        x.__dict__.update(entries)
    return x
