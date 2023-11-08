from abc import ABC, abstractmethod


class Base(ABC):
    @abstractmethod
    def __patch(self, data):
        return

    @abstractmethod
    def to_json(self):
        return
