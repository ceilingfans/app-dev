from Base import Base


class User(Base):
    """
    User structure:
    User {
      id: str(uuid),
      name: str,
      email: str,
      password: Hash(str),
      address: Address { ... },
      subscription: {
        plan: PlanType,
        duration: {
          start: time,
          end: time,
          length: time,
        }
      }
    }
    """
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
