
class Billinghistory:
    __customerid: str = None
    __billid: str = None
    __status: bool = None

    def __init__(self, data):
        self.__customerid = data.get("customerid", None)
        self.__billid = data.get("billid", None)
        self.__status = data.get("status", None)

    # use dict(<User>) to get the JSON
    def __iter__(self):
        yield 'customerid', self. __customerid
        yield 'billid', self.__billid
        yield 'status',self.__status

    def get_customerid(self):
        return self.__customerid

    def get_status(self):
        return self.__status

    def get_billid(self):
        return self.__billid



