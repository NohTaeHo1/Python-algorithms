from abc import *


class EditorBase(metaclass=ABCMeta):
    @abstractmethod
    def dropna(self, this):
        pass


class PrinterBase(metaclass=ABCMeta):
    @abstractmethod
    def print(self):
        pass

    @abstractmethod
    def dframe(self, this):
        pass


class ReaderBase(PrinterBase):

    @abstractmethod
    def csv(self, file):
        pass

    @abstractmethod
    def excel(self, file, header, usecols):
        pass

    @abstractmethod
    def json(self, file):
        pass

    @abstractmethod
    def gmaps(self, api_key: str):
        pass


class ScraperBase(metaclass=ABCMeta):
    @abstractmethod
    def driver(self):
        pass

    @abstractmethod
    def auto_login(self, driver, url, selector, data):
        pass
