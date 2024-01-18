from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")

CONNECTION_STRING=f"CONNECTION_STRING + {password}"

class Database:
    def __init__(self, dbname: str):
        MONGO_URL = CONNECTION_STRING
        try:
            mongo_client = MongoClient(MONGO_URL)
            mongo_client.server_info()
            self.client = mongo_client
        except ConnectionFailure:
            print("Invalid Mongo DB URL. Please Check Your Credentials! Exiting...")
            quit(1)
        print("Connection Successful")
        self.dbname = dbname

class DatabaseCollection(Database):
    def __init__(self, dbname, dbcol):
        super().__init__(dbname)
        self.dbcol = dbcol
    def get_database(self):
        db = self.client[self.dbname]
        collection = db[f"{self.dbcol}"]
        return collection





