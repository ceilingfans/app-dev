from pymongo import MongoClient
from pymongo.errors import OperationFailure
from pymongo.database import Database
from pymongo.server_api import ServerApi
from dotenv import load_dotenv, find_dotenv
import os

from api.structures.User import User

# load env vars to our system
load_dotenv(find_dotenv())

# MongoDB things
ALREADY_RUNNING = False


# TODO: proper error handling
class Driver:
    client: MongoClient
    db: Database

    def __init__(self, dev: bool = True):
        if ALREADY_RUNNING:
            print("error: db driver class has already been initiated")  # TODO: logging
            exit(1)

        self.__create_client()
        self.__get_db(dev)

    def create_user(self, user: User):
        existing = self.get_user_by_id(user.get_id())
        if existing:
            print(f"error: user with id {user.get_id()} already exists")
            return

        try:
            self.db["users"].insert_one(dict(user))
            print(f"info: created user with id {user.get_id()}")
        except OperationFailure:
            print("error: OperationFailure from create_user")

    def get_user_by_id(self, user_id: str = None):  # TODO: accept id or email, change name to get_user
        if user_id is None:
            return list(self.db["users"].find())

        result = self.db["users"].find_one({"id": user_id})
        if result:
            return result

        print("info: user not found")

    def update_user(self, new_user: User):
        try:
            result = self.db["users"].find_one_and_update({"id": new_user.get_id()}, {"$set": dict(new_user)})
            if result is None:
                print(f"error: user with id {new_user.get_id()} not found")
                return

            else:
                print(f"info: update user with id {new_user.get_id()}")
                return result

        except OperationFailure:
            print("error: OperationFailure from update_user_by_id")

    def delete_user_by_id(self, user_id: str):
        try:
            result = self.db["users"].delete_one({"id": user_id})

            if result.deleted_count == 0:
                print(f"error: user with id {user_id} not found")
            else:
                print(f"info: deleted user with id {user_id}")

            return bool(result.deleted_count)

        except OperationFailure:
            print("error: OperationFailure from delete_user_by_id")

    def __create_client(self):
        global ALREADY_RUNNING

        uri = os.environ.get("MONGO_CONNECTION_STRING")

        if not uri:
            print("error: MONGO_CONNECTION_STRING env cannot be found")  # TODO: logging
            exit(1)

        client = MongoClient(uri, server_api=ServerApi('1'))
        try:
            print("info:", client.server_info())
            print("info: connected to server")
        except Exception as e:
            print("error:\n" + str(e))

        ALREADY_RUNNING = True
        self.client = client

    def __get_db(self, dev):
        if dev:
            self.db = self.client.dev
        else:
            self.db = self.client.master


# test code, ignore pls
if __name__ == "__main__":
    total = 0
    passed = 0

    print("test: connect to db")
    total += 1
    db = Driver()
    passed += 1
    print("------------------------------------------------------------\n\n")

    # print("test: try double instance of Driver")
    # Driver()
    # print("------------------------------------------------------------\n\n")

    print("test: find user by id")
    total += 1
    print(db.get_user_by_id("3d1919bb-4d0b-497e-822f-1bba586d54c2"))
    passed += 1
    print("------------------------------------------------------------\n\n")

    print("test: find all users")
    total += 1
    print(db.get_user_by_id())
    passed += 1
    print("------------------------------------------------------------\n\n")

    print("test: create a user")
    total += 1
    user = User({
        "name": "Jane Doe",
        "password": "9cd9ec4c865145c4fa2ea654bbccb7ee",
        "id": "d8ed0e07-54b9-4205-ac64-d9e16b152f82",
        "email": "jane_doe@gmail.com",
        "address": "1913 Rosebud Dr, Maryville, Tennessee(TN), 37803",
        "subscription": {
            "plan": "Bronze",
            "duration": {
                "start": 1704464537925,
                "end": 1712353937925,
                "length": 7889400000
            }
        }
    })
    print(dict(user))
    db.create_user(user)
    passed += 1
    print("------------------------------------------------------------\n\n")

    print("test: update a user")
    total += 1
    new_user = User({
        "name": "Jane Doe",
        "password": "9cd9ec4c865145c4fa2ea654bbccb7ee",
        "id": "d8ed0e07-54b9-4205-ac64-d9e16b152f82",
        "email": "jane_doe@gmail.com",
        "address": "38042 28th Ave, Gobles, Michigan(MI), 49055",  # address change
        "subscription": {
            "plan": "Bronze",
            "duration": {
                "start": 1704464537925,
                "end": 1712353937925,
                "length": 7889400000
            }
        }
    })
    db.update_user(new_user)
    passed += 1
    print("------------------------------------------------------------\n\n")

    print("test: delete a user")
    total += 1
    db.delete_user_by_id("d8ed0e07-54b9-4205-ac64-d9e16b152f82")
    passed += 1
    print("------------------------------------------------------------\n\n")

    # write tests above this
    print(f"Total tests: {total}\nPassed: {passed}\nFailed: {total-passed}\nIf there are no errors then the tests "
          f"should have all passed yippie")