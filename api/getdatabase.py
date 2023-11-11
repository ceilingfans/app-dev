from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")

CONNECTION_STRING=f"YOUR_MONGO_STRING + f{password}"

def get_userdatabase():
    
    MONGO_URL = CONNECTION_STRING
    
    try:
        mongo_client = MongoClient(MONGO_URL)
        mongo_client.server_info()
    except ConnectionFailure:
        print("Invalid Mongo DB URL. Please Check Your Credentials! Exiting...")
        quit(1)
    print("Connection Successful")
    
    return mongo_client['user_list']
#Add second DB.
def get_inventorydatabase():
    return

if __name__ == "__main__":   
   
   userdb = get_userdatabase()
#  invdb = get_inventorydatabase()






