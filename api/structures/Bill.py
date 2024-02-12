class Bill:
    __customer_id: str = None
    __bill_id: str = None
    __status: bool = None
    __price : float = None
    __plan : str = None

    def __init__(self, data):
        self.__customer_id = data.get("customer_id", None)
        self.__bill_id = data.get("bill_id", None)
        self.__price = data.get("price", None)
        self.__status = data.get("status", None)
        self.__plan = data.get("plan", None)

    # use dict(<User>) to get the JSON
    def __iter__(self):
        yield 'customer_id', self. __customer_id
        yield 'bill_id', self.__bill_id
        yield 'status',self.__status
        yield 'price',self.__price
        yield 'plan',self.__plan

    def get_customer_id(self):
        return self.__customer_id

    def get_status(self):
        return self.__status

    def get_bill_id(self):
        return self.__bill_id

    def get_price(self):
        return self.__price
    
    def get_plan(self):
        return self.__plan


