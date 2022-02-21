from multirunnable._singletons import NamedSingletonABCMeta

from abc import ABCMeta



class BasePersistence(metaclass=NamedSingletonABCMeta):
    pass



class DataPersistenceLayer(metaclass=ABCMeta):
    pass

