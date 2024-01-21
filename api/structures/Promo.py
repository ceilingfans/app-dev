from enum import Enum, auto


class PromoType(Enum):
    Percentage = auto()  # x%
    Value = auto()  # $x


class Promo:
    __id: str = None
    __type: PromoType = None
    # if type is Percentage, interpret value as the percentage discount
    # if type is Value, interpret value as the amount deducted from the final price
    __value: int = None
    __expire: int = None

    def __init__(self, data):
        self.__id = data.get("id")
        self.__type = PromoType[data.get("type")]
        self.__value = int(data.get("value"))
        self.__expire = int(data.get("expire"))

    def __iter__(self):
        yield "id", self.__id
        yield "type", self.__type.name
        yield "value", self.__value
        yield "expire", self.__expire

    def get_id(self):
        return self.__id

    def get_type(self):
        return self.__type

    def get_value(self):
        return self.__value

    def get_expire(self):
        return self.__expire