from pymongo import MongoClient
from pymongo.database import Database
from pymongo.server_api import ServerApi
from dotenv import load_dotenv, find_dotenv
import os
import uuid

# TODO: fix pathing issue, (please do not commit any hotfixes)

from UserManager import UserManager
from PromoManager import PromoManager
from ItemManager import ItemManager
from PlanManager import PlanManager
from BillManager import BillManager

# load env vars to our system
load_dotenv(find_dotenv())

# MongoDB things
ALREADY_RUNNING = False


# TODO: proper error handling
def generate_id():
    return str(uuid.uuid4())


class Driver:
    client: MongoClient
    db: Database
    users: UserManager

    def __init__(self, dev: bool = True):
        if ALREADY_RUNNING:
            print("error: db driver class has already been initiated")  # TODO: logging
            exit(1)

        # generate essentials
        self.__create_client()
        self.__get_db(dev)

        # managers
        self.users = UserManager(self.client, self.db["users"])
        self.promos = PromoManager(self.client, self.db["promos"])
        self.items = ItemManager(self.client, self.db["insured_items"])
        self.plans = PlanManager(self.client, self.db["plan_descriptions"])
        self.bills = BillManager(self.client, self.db["bills"])

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
