from enum import Enum, auto
from structures.Base import Base


# TODO: create validators and errors to handle bad data

class PlanKind(Enum):
    # TODO: use actual subscription plans
    Bronze = auto()
    Silver = auto()
    Gold = auto()


class Duration(Base):
    __start: int
    __end: int
    __length: int

    def __init__(self, data):
        self.__patch(data)

    def __patch(self, data):
        if data is None:
            return

        self.__start = data.start
        self.__end = data.end
        self.__length = data.length

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
    __plan: PlanKind
    __duration: Duration

    def __init__(self, data):
        self.__patch(data)

    def __patch(self, data):
        if data is None:
            return

        self.__plan = PlanKind[data.plan]
        self.__duration = Duration(data.duration)

    def __iter__(self):
        yield 'plan', self.__plan.name
        yield 'duration', dict(self.__duration)


class User(Base):
    __name: str
    __password: str  # TODO: make this hashed
    __id: str
    __email: str
    __address: str
    __subscription: Subscription

    def __init__(self, data):
        self.__patch(data)

    def __patch(self, data):
        if data is None:
            return

        self.__name = data.name
        self.__password = data.password
        self.__id = data.id
        self.__email = data.email
        self.__address = data.address
        self.__subscription = data.subscription

        return self

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
