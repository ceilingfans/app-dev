from pymongo import MongoClient
from pymongo.database import Database
from pymongo.server_api import ServerApi
from dotenv import load_dotenv, find_dotenv
import os


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
    print("test: connect to db")
    db = Driver()
    print("------------------------------------------------------------\n\n")

    print("test: try double instance of Driver")
    Driver()
    print("------------------------------------------------------------\n\n")
