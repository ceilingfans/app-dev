class Damage:
    __description: str = None
    __date: int = None

    def __init__(self, data: dict):
        self.__description = data.get("description", None)
        self.__date = data.get("date", None)

    def __iter__(self):
        yield 'description', self.__description
        yield 'date', self.__date


# TODO: find out what to put in each repair report
class Repair:
    def __init__(self, data):
        pass

    def __iter__(self):
        pass


class RepairStatus:
    __past_repairs: list[Repair] = []
    __current: Repair = None

    def __init__(self, data: dict):
        self.__past_repairs = list(map(lambda x: Repair(x), data.get("past_repairs", [])))
        self.__current = data.get("current", None)

    def __iter__(self):
        yield 'past_repairs', self.__past_repairs
        yield 'current', self.__current


# TODO: find out what location data to save
class Location:
    def __init__(self, data):
        pass

    def __iter__(self):
        pass


class ItemStatus:
    __damage: Damage = None
    __repair_status: RepairStatus = None
    __location: Location = None

    def __init__(self, data: dict):
        self.__damage = data.get("damage", None)
        self.__repair_status = data.get("repair_status", None)
        self.__location = data.get("location", None)

    def __iter__(self):
        yield 'damage', self.__damage
        yield 'repair_status', self.__repair_status
        yield 'location', self.__location


class InsuredItem:
    __owner_id: str = None
    __item_id: str = None
    __status: ItemStatus = None

    def __init__(self, data: dict):
        self.__owner_id = data.get("owner_id", None)
        self.__item_id = data.get("item_id", None)
        self.__status = data.get("status", None)

    def __iter__(self):
        yield 'owner_id', self.__owner_id
        yield 'item_id', self.__item_id
        yield 'status', self.__status
