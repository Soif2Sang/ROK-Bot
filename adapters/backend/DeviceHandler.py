from abc import ABC, abstractmethod

from numpy import ndarray


class DeviceHandler(ABC):
    @abstractmethod
    def get_screen(self):
        pass

    @abstractmethod
    def find_img(self, target: str, source: ndarray = None, confidence: float = 0.8):
        pass

    @abstractmethod
    def find_multiple_img(self, target: str, source: ndarray = None, confidence: float = 0.8):
        pass

    @abstractmethod
    def click(self, x: int, y: int):
        pass

    @abstractmethod
    def swipe(self, x: int, y: int, x2: int, y2: int):
        pass