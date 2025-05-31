from abc import ABC, abstractmethod

from numpy import ndarray

class FrontEndAdapter(ABC):
    @abstractmethod
    def __init__(self, device_id, **kwargs):
        pass

    @abstractmethod
    def set_status(self, text: str):
        pass

    @abstractmethod
    def get_status(self) -> str:
        pass

    @abstractmethod
    def log(self, text: str, color = None):
        pass