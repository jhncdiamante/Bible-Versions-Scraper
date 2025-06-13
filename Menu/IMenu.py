from abc import ABC, abstractmethod

class IMenu(ABC):
    @abstractmethod
    def open(self): pass

    @abstractmethod
    def getAllBookElements(self): pass
    