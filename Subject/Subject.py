# observer_pattern.py
from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, data: dict):
        pass

class Subject(ABC):
    def __init__(self):
        self._observer: Observer | None = None

    def attach(self, observer: Observer):
        self._observer = observer

    def notify(self):
        self._observer.update(self.current_data)
