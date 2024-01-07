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

    def __init__(self, data):
        self.__id = data.get("id")
        self.__type = PromoType[data.get("type")]
        self.__value = int(data.get("value"))

    def __iter__(self):
        yield "id", self.__id
        yield "type", self.__type.name
        yield "value", self.__value

    def get_id(self):
        return self.__id

    def get_type(self):
        return self.__type

    def get_value(self):
        return self.__value
