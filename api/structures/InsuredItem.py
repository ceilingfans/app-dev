from enum import Enum, auto


# TODO: create validators and errors to handle bad data

class PlanKind(Enum):
    # TODO: use actual subscription plans
    Bronze = auto()
    Silver = auto()
    Gold = auto()


class Duration:
    __start: int = None
    __end: int = None
    __length: int = None

    def __init__(self, data):
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


class Subscription:
    __plan: PlanKind = None
    __duration: Duration = None

    def __init__(self, data):
        self.__plan = PlanKind[data.get("plan", None)]
        self.__duration = Duration(data.get("duration", None))

    def __iter__(self):
        yield 'plan', self.__plan.name
        yield 'duration', dict(self.__duration)

    def get_plan(self):
        return self.__plan

    def get_duration(self):
        return self.__duration


class Damage:
    __description: str = None
    __date: int = None

    def __init__(self, data):
        self.__description = data.get("description", None)
        self.__date = data.get("date", None)

    def __iter__(self):
        yield 'description', self.__description
        yield 'date', self.__date

    def get_description(self):
        return self.__description

    def get_date(self):
        return self.__date


# TODO: find out what to put in each repair report
class Repair:
    __description: str = None
    # all dates use unix timestamp
    __start_date: int = None
    __end_date: int = None

    def __init__(self, data):
        self.__description = data.get("description", None)
        self.__start_date = data.get("start_date", None)
        self.__end_date = data.get("end_date", None)

    def __iter__(self):
        yield 'description', self.__description
        yield 'start_date', self.__start_date
        yield 'end_date', self.__end_date

    def get_description(self):
        return self.__description

    def get_start_date(self):
        return self.__start_date

    def get_end_date(self):
        return self.__end_date


class RepairStatus:
    __past_repairs: list[Repair] = []
    __current: Repair = None

    def __init__(self, data):
        self.__past_repairs = [Repair(i) for i in data.get("past_repairs")]
        self.__current = Repair(data.get("current", None))

    def __iter__(self):
        yield 'past_repairs', [dict(i) for i in self.__past_repairs]
        yield 'current', dict(self.__current)

    def get_past_repairs(self):
        return self.__past_repairs

    def get_current(self):
        return self.__current


class ItemStatus:
    __damage: Damage = None
    __repair_status: RepairStatus = None
    __address: str = None

    def __init__(self, data):
        self.__damage = Damage(data.get("damage", None))
        self.__repair_status = RepairStatus(data.get("repair_status", None))
        self.__address = data.get("address", None)

    def __iter__(self):
        yield 'damage', dict(self.__damage)
        yield 'repair_status', dict(self.__repair_status)
        yield 'address', self.__address

    def get_damage(self):
        return self.__damage

    def get_repair_status(self):
        return self.__repair_status

    def get_address(self):
        return self.__address


class InsuredItem:
    __owner_id: str = None
    __item_id: str = None
    __status: ItemStatus = None
    __subscription: Subscription = None

    def __init__(self, data):
        self.__owner_id = data.get("owner_id", None)
        self.__item_id = data.get("item_id", None)
        self.__status = ItemStatus(data.get("status", None))
        self.__subscription = Subscription(data.get("subscription", None))

    def __iter__(self):
        yield 'owner_id', self.__owner_id
        yield 'item_id', self.__item_id
        yield 'status', dict(self.__status)
        yield 'subscription', dict(self.__subscription)

    def get_owner_id(self):
        return self.__owner_id

    def get_item_id(self):
        return self.__item_id

    def get_status(self):
        return self.__status

    def get_subscription(self):
        return self.__subscription
