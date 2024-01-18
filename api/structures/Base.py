from abc import ABC, abstractmethod


class Base(ABC):
    """
    Provides an abstract method that allows for dict() to be used to convert the instance to a dict (JSON).
    """

    @abstractmethod
    def __iter__(self):
        return
