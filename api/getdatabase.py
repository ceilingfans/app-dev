from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo import MongoClient

def get_userdatabase():

    CONNECTION_STRING="YOUR_MONGO_STRING"
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
'''
def get_inventorydatabase():

    CONNECTION_STRING="YOUR MONGO STRING"
    MONGO_URL = CONNECTION_STRING
    
    try:
        mongo_client = MongoClient(MONGO_URL)
        mongo_client.server_info()
    except ConnectionFailure:
        print("Invalid Mongo DB URL. Please Check Your Credentials! Exiting...")
        quit(1)
    
    
    return mongo_client['inventory_list']
'''
    
if __name__ == "__main__":   
   
   userdb = get_userdatabase()
#  invdb = get_inventorydatabase()
   
   
    
    




