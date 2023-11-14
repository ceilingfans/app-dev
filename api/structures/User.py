from enum import Enum, auto
from Base import Base


# TODO: create validators and errors to handle bad data

class PlanKind(Enum):
    # TODO: use actual subscription plans
    Bronze = auto()
    Silver = auto()
    Gold = auto()


class Duration(Base):
    __start: int = None
    __end: int = None
    __length: int = None

    def __init__(self, data: dict):
        self.__start = data.get("start", None)
        self.__end = data.get("end", None)
        self.__length = data.get("length", None)

    def __iter__(self):
        yield 'start', self.__start
        yield 'end', self.__end
        yield 'length', self.__length

    def get_start(self):
        return self.__start

    def get_end(self):
        return self.__end

    def get_length(self):
        return self.__length


class Subscription(Base):
    __plan: PlanKind = None
    __duration: Duration = None

    def __init__(self, data: dict):
        self.__plan = PlanKind[data.get("plan", None)]
        self.__duration = Duration(data.get("duration", None))

    def __iter__(self):
        yield 'plan', self.__plan.name
        yield 'duration', dict(self.__duration)


class User(Base):
    __name: str = None
    __password: str = None  # TODO: make this hashed
    __id: str = None
    __email: str = None
    __address: str = None
    __subscription: Subscription = None

    def __init__(self, data: dict):
        self.__name = data.get("name", None)
        self.__password = data.get("password", None)
        self.__id = data.get("id", None)
        self.__email = data.get("email", None)
        self.__address = data.get("address", None)
        self.__subscription = data.get("subscription", None)

    # use dict(<User>) to get the JSON
    def __iter__(self):
        yield 'name', self.__name
        yield 'password', self.__password
        yield 'id', self.__id
        yield 'email', self.__email
        yield 'address', self.__address
        yield 'subscription', self.__subscription

    def get_name(self):
        return self.__name

    def get_password(self):
        return self.__password

    def get_id(self):
        return self.__id

    def get_email(self):
        return self.__email

    def get_address(self):
        return self.__address

    def get_subscription(self):
        return self.__subscription
