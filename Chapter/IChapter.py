from abc import ABC, abstractmethod

class IChapter(ABC):
    @abstractmethod
    def getAllVerses(self): pass