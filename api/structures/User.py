class User:
    __name: str = None
    __password: str = None  # TODO: make this hashed
    __id: str = None
    __email: str = None
    __address: str = None

    def __init__(self, data):
        self.__name = data.get("name", None)
        self.__password = data.get("password", None)
        self.__id = data.get("id", None)
        self.__email = data.get("email", None)
        self.__address = data.get("address", None)

    # use dict(<User>) to get the JSON
    def __iter__(self):
        yield 'name', self.__name
        yield 'password', self.__password
        yield 'id', self.__id
        yield 'email', self.__email
        yield 'address', self.__address

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
