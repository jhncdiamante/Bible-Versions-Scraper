from abc import ABC, abstractmethod

class IBook(ABC):
    @abstractmethod
    def getAllChapterElements(self): pass

    @abstractmethod
    def getName(self): pass