from abc import ABC, abstractmethod


class Base(ABC):
    @abstractmethod
    def __patch(self, data):
        return

    @abstractmethod
    def __iter__(self):
        return
