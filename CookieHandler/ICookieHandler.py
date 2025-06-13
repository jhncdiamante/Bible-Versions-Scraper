from abc import ABC, abstractmethod

class ICookieHandler(ABC):
    @abstractmethod
    def clickAllowCookiesButton(self): pass