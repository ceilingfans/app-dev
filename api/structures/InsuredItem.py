from Base import Base


class Damage(Base):
    __description: str
    __date: int

    def __init__(self, data):
        self.__patch(data)

    def __patch(self, data):
        self.__description = data.description
        self.__date = data.date

    def __iter__(self):
        yield 'description', self.__description
        yield 'date', self.__date


# TODO: find out what to put in each repair report
class Repair(Base):
    def __init__(self):
        pass

    def __patch(self, data):
        pass

    def __iter__(self):
        pass


class RepairStatus(Base):
    __past_repairs: list[Repair]
    __current: Repair

    def __init__(self, data):
        self.__patch(data)

    def __patch(self, data):
        self.__past_repairs = data.past_repairs
        self.__current = data.current

    def __iter__(self):
        yield 'past_repairs', self.__past_repairs
        yield 'current', self.__current


# TODO: find out what location data to save
class Location(Base):
    def __init__(self, data):
        self.__patch(data)

    def __patch(self, data):
        pass

    def __iter__(self):
        pass


class ItemStatus(Base):
    __damage: Damage
    __repair_status: RepairStatus
    __location: Location

    def __init__(self, data):
        self.__patch(data)

    def __patch(self, data):
        self.__damage = data.damage
        self.__repair_status = data.repair_status
        self.__location = data.location

    def __iter__(self):
        yield 'damage', self.__damage
        yield 'repair_status', self.__repair_status
        yield 'location', self.__location


class InsuredItem(Base):
    __owner_id: str
    __item_id: str
    __status: ItemStatus

    def __init__(self, data):
        self.__patch(data)

    def __patch(self, data):
        self.__owner_id = data.owner_id
        self.__item_id = data.item_id
        self.__status = data.status

    def __iter__(self):
        yield 'owner_id', self.__owner_id
        yield 'item_id', self.__item_id
        yield 'status', self.__status
