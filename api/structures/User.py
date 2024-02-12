from argon2 import PasswordHasher
from flask_login import UserMixin

ph = PasswordHasher()


class User(UserMixin):
    __name: str = None
    __password: str = None
    __id: str = None
    __email: str = None
    __address: str = None
    __newuser: bool = True
    __picture:  str = None
    __currentplan: str = None
    __products: list = None
    

    def __init__(self, data):
        self.__name = data.get("name", None)
        self.__password = data.get("password", None)
        self.__id = data.get("id", None)
        self.__email = data.get("email", None)
        self.__address = data.get("address", None)
        self.__newuser = data.get("newuser", None)
        self.__picture = data.get("picture", None)
        self.__currentplan = data.get("currentplan", None)
        self.__products = data.get("products", None)
    # use dict(<User>) to get the JSON
    def __iter__(self):
        yield 'name', self.__name
        yield 'password', self.__password
        yield 'id', self.__id
        yield 'email', self.__email
        yield 'address', self.__address
        yield 'newuser', self.__newuser
        yield 'picture', self.__picture
        yield 'currentplan', self.__currentplan
        yield 'products', self.__products

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
    
    def get_newuser(self):
        return self.__newuser
    
    def get_picture(self):
        return self.__picture
    
    def get_currentplan(self):
        return self.__currentplan
    
    def get_products(self):
        return self.__products
    



def get_hash(password):
    return ph.hash(password)


def check_hash(password, hash):
    return ph.verify(hash, password)
