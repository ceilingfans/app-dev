from pymongo import MongoClient, ReturnDocument
from pymongo.errors import OperationFailure
from pymongo.database import Database
from pymongo.server_api import ServerApi
from dotenv import load_dotenv, find_dotenv
import os
# Shit doesnt work for me without manually setting path ~ Isaac
import sys
import uuid

# sys.path.insert(1, "C://Users//mdame//OneDrive//Desktop//School//Sem 2//AppDevelopment//app-dev//api")

#sys.path.insert(1, "G://app-dev//app-dev//api")

from api.structures.User import User
from api.structures.Promo import Promo
from api.structures.InsuredItem import InsuredItem, PlanKind
from api.structures.PlanDescription import PlanDescription
from api.structures.billinghistory import Billinghistory

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
        
    def generate_id(self):
        return str(uuid.uuid4())

    # User CRUD
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

    # returns a user if `user_id` is provided and is found, else returns entire `users` collection in a list
    def get_user_by_id(self, user_id: str = None):  # TODO: accept id or email, change name to get_user
        if user_id is None:
            return list(self.db["users"].find())

        result = self.db["users"].find_one({"id": user_id})
        if result:
            return result

        print("info: user not found")

    def update_user(self, new_user: User):
        try:
            result = self.db["users"].find_one_and_update({"id": new_user.get_id()}, {"$set": dict(new_user)},
                                                          return_document=ReturnDocument.AFTER)
            if result is None:
                print(f"error: user with id {new_user.get_id()} not found")
                return

            print(f"info: update user with id {new_user.get_id()}")
            return result

        except OperationFailure:
            print("error: OperationFailure from update_user")

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

    # END of User CRUD
    # Promo CRUD
    def create_promo(self, promo: Promo):
        existing = self.find_promo_by_id(promo.get_id())
        if existing:
            print(f"error: promo with id {promo} already exists")
            return

        try:
            self.db["promos"].insert_one(dict(promo))
            print(f"info: promo with id {promo.get_id()} created")
        except OperationFailure:
            print("error: OperationFailure in create_promo")

    # returns a promo if `promo_id` is provided and found, else returns the entire `promos` collection in a list
    def find_promo_by_id(self, promo_id: str = None):
        if promo_id is None:
            return list(self.db["promos"].find())

        result = self.db["promos"].find_one({"id": promo_id})
        if result:
            return result

        print(f"info: promo with id {promo_id} not found")

    def update_promo(self, new_promo: Promo):
        try:
            result = self.db["promos"].find_one_and_update({"id": new_promo.get_id()}, {"$set": dict(new_promo)},
                                                           return_document=ReturnDocument.AFTER)
            if result is None:
                print(f"error: promo with id {new_promo.get_id()} not found")
                return

            print(f"info: update promo with id {new_promo.get_id()}")
            return result

        except OperationFailure:
            print("error: OperationFailure from update_promo_by_id")

    def delete_promo_by_id(self, promo_id: str):
        try:
            result = self.db["promos"].delete_one({"id": promo_id})

            if result.deleted_count == 0:
                print(f"error: promo with id {promo_id} not found")
            else:
                print(f"info: deleted promo with id {promo_id}")

            return bool(result.deleted_count)

        except OperationFailure:
            print("error: OperationFailure from delete_promo_by_id")

    # END of Promo CRUD
    # InsuredItem CRUD
    def create_insured_item(self, insured_item: InsuredItem):
        existing = self.find_insured_item(item_id=insured_item.get_item_id())
        if existing:
            print(f"error: item with id {insured_item.get_item_id()} already exists")
            return

        try:
            self.db["insured_items"].insert_one(dict(insured_item))
            print(f"info: item with id {insured_item.get_item_id()} created")
        except OperationFailure:
            print("error: OperationFailure in create_insured_item")

    def find_insured_item(self, item_id: str = None, owner_id: str = None):
        if item_id is not None:
            query = {"item_id": item_id}
        elif owner_id is not None:
            query = {"owner_id": owner_id}
        else:
            print("error: either item_id or owner_id is required")
            return

        return self.db["insured_items"].find_one(query)

    def update_insured_item(self, new_insured_item: InsuredItem):
        try:
            result = self.db["insured_items"].find_one_and_update({"item_id": new_insured_item.get_item_id()},
                                                                  {"$set": dict(new_insured_item)},
                                                                  return_document=ReturnDocument.AFTER)

            if result is None:
                print(f"error: item with id {new_insured_item.get_item_id()} does not exist")
                return

            print(f"info: update insured item with id {new_insured_item.get_item_id()}")
            return result

        except OperationFailure:
            print("error: OperationFailure in update_insured_item")
            return

    def delete_insured_item_by_id(self, item_id: str):
        try:
            result = self.db["insured_items"].delete_one({"item_id": item_id})

            if result.deleted_count == 0:
                print(f"error: item with id {item_id} not found")
            else:
                print(f"info: deleted item with id {item_id}")

            return bool(result.deleted_count)

        except OperationFailure:
            print("error: OperationFailure from delete_insured_item_by_id")

    # END of InsuredItem CRUD
    # PlanDescription CRUD
    def create_plan(self, plan: PlanDescription):
        existing = self.find_plan_by_type(plan.get_plan_type().name)
        if existing:
            print(f"error: plan with name {plan.get_plan_type().name} already exists")
            return

        try:
            self.db["plan_descriptions"].insert_one(dict(plan))
            print(f"info: plan with id {plan.get_plan_type().name} created")
        except OperationFailure:
            print("error: OperationFailure in create_plan")

    def find_plan_by_type(self, plan_type: PlanKind = None):
        if plan_type is None:
            return self.db["plan_descriptions"].find()

        result = self.db["plan_descriptions"].find_one({"plan_type": plan_type.name})
        if result:
            return result

        print(f"info: plan with type {plan_type.name} not found")

    def update_plan(self, new_plan: PlanDescription):
        try:
            result = self.db["plan_descriptions"].find_one_and_update({"plan_type": new_plan.get_plan_type().name},
                                                                  {"$set": dict(new_plan)},
                                                                  return_document=ReturnDocument.AFTER)

            if result is None:
                print(f"error: plan with type {new_plan.get_plan_type().name} does not exist")
                return

            print(f"info: update plan with type {new_plan.get_plan_type().name}")
            return result

        except OperationFailure:
            print("error: OperationFailure in update_plan")
            return

    # do not use this unless it is really needed
    def delete_plan_by_type(self, plan_type: PlanKind):
        try:
            result = self.db["plan_description"].delete_one({"plan_type": plan_type.name})

            if result.deleted_count == 0:
                print(f"error: plan with type {plan_type.name} not found")
            else:
                print(f"info: deleted plan with type {plan_type.name}")

            return bool(result.deleted_count)

        except OperationFailure:
            print("error: OperationFailure from delete_plan_by_type")
            
    #End of PlanDescription CRUD
    #Billinghistory CRUD
    def create_bill(self,bill: Billinghistory):
        existing = self.get_bill_by_id(bill.get_billid())
        if existing:
            print(f"error: user with id {bill.get_billid()} already exists")
            return
        try:
            self.db["billinghistory"].insert_one(dict(bill))
            print(f"info: created bill with id {bill.get_billid()}")
        except OperationFailure:
            print("error: OperationFailure from create_bill")
        return
    
    def get_bill_by_id(self, bill_id: str = None): 
        if bill_id is None:
            return list(self.db["billinghistory"].find())

        result = self.db["billinghistory"].find_one({"billid": bill_id})
        if result:
            return result
    
    # USE TO UPDATE PAYMENT STATUS
    def update_bill(self, new_bill: Billinghistory):
        try:
            result = self.db["billinghistory"].find_one_and_update({"billid": new_bill.get_billid()}, {"$set": dict(new_bill)},
                                                          return_document=ReturnDocument.AFTER)
            if result is None:
                print(f"error: bill with id {new_bill.get_billid()} not found")
                return

            print(f"info: update bill with id {new_bill.get_billid()}")
            return result

        except OperationFailure:
            print("error: OperationFailure from update_bill")
        
        return
    
    def delete_bill_by_id(self, bill_id: str):
        try:
            result = self.db["billinghistory"].delete_one({"billid": bill_id})

            if result.deleted_count == 0:
                print(f"error: bill with id {bill_id} not found")
            else:
                print(f"info: deleted bill with id {bill_id}")

            return bool(result.deleted_count)

        except OperationFailure:
            print("error: OperationFailure from delete_bill_by_id")
    
    def get_bill_info(self,bill:Billinghistory): #TODO get Bill details from other DBs.
        return
    
    #End of Billing CRUD
    
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
    })
    db.update_user(new_user)
    passed += 1
    print("------------------------------------------------------------\n\n")

    print("test: delete a user")
    total += 1
    db.delete_user_by_id("d8ed0e07-54b9-4205-ac64-d9e16b152f82")
    passed += 1
    print("------------------------------------------------------------\n\n")

    print("test: create a promo")
    total += 1
    promo = Promo({
        "id": "XMAS20",
        "type": "Percentage",
        "value": 20
    })
    db.create_promo(promo)
    passed += 1
    print("------------------------------------------------------------\n\n")

    print("test: find a promo by id")
    total += 1
    p = db.find_promo_by_id("XMAS20")
    if p is not None:
        print(p)
        passed += 1
    print("------------------------------------------------------------\n\n")

    print("test: update a promo")
    total += 1
    new_promo = Promo({
        "id": "XMAS20",
        "type": "Value",
        "value": 20
    })
    updated = db.update_promo(new_promo)
    if updated is not None:
        print(updated)
        passed += 1
    print("------------------------------------------------------------\n\n")

    print("test: delete promo")
    total += 1
    if db.delete_promo_by_id("XMAS20"):
        passed += 1
    print("------------------------------------------------------------\n\n")

    print("test: create insured item")
    total += 1
    item = InsuredItem({
        "owner_id": "3d1919bb-4d0b-497e-822f-1bba586d54c2",
        "item_id": "fda25a81-b823-4d9a-a526-94781e301a20",
        "status": {
            "damage": {
                "description": "Phone has a crack on the bottom left front screen",
                "date": 1704537866402
            },
            "repair_status": {
                "past_repairs": [],
                "current": {
                    "description": "Sent to our specialists for repair",
                    "start_date": 1704538866402,
                    "end_date": None
                }
            },
            "address": "1117 Willow St, Eden, North Carolina(NC), 27288"
        },
        "subscription": {
            "plan": "Bronze",
            "duration": {
                "start": 1704464537925,
                "end": 1712353937925,
                "length": 7889400000
            }
        }
    })
    db.create_insured_item(item)
    passed += 1
    print("------------------------------------------------------------\n\n")

    print("test: find item by id")
    total += 1
    i = db.find_insured_item(item_id="fda25a81-b823-4d9a-a526-94781e301a20")
    if i is not None:
        print(i)
        passed += 1
    print("------------------------------------------------------------\n\n")

    print("test: update item")
    total += 1
    new_item = InsuredItem({
        "owner_id": "3d1919bb-4d0b-497e-822f-1bba586d54c2",
        "item_id": "fda25a81-b823-4d9a-a526-94781e301a20",
        "status": {
            "damage": {
                "description": "Phone has a crack on the bottom left front screen",
                "date": 1704537866402
            },
            "repair_status": {
                "past_repairs": [],
                "current": {
                    "description": "Started repairs, ETA: 1 week",
                    "start_date": 1704538866402,
                    "end_date": None
                }
            },
            "address": "1117 Willow St, Eden, North Carolina(NC), 27288"
        },
        "subscription": {
            "plan": "Bronze",
            "duration": {
                "start": 1704464537925,
                "end": 1712353937925,
                "length": 7889400000
            }
        }
    })
    updated = db.update_insured_item(new_item)
    if updated is not None:
        print(updated)
        passed += 1
    print("------------------------------------------------------------\n\n")

    print("test: delete item")
    total += 1
    if db.delete_insured_item_by_id("fda25a81-b823-4d9a-a526-94781e301a20"):
        passed += 1
    print("------------------------------------------------------------\n\n")
    
    print("test: create a bill")
    total += 1
    bill = Billinghistory({
        "customerid": "d8ed0e07-54b9-4205-ac64-d9e16b152f82",
        "billid": "7070",
        "status": False,
    })
    print(dict(bill))
    db.create_bill(bill)
    passed += 1
    print("------------------------------------------------------------\n\n")
    print("test: update a bill")
    total += 1
    new_bill = Billinghistory({
        "customerid": "d8ed0e07-54b9-4205-ac64-d9e16b152f82",
        "billid": "7070",
        "status": True,
    })
    print("------------------------------------------------------------\n\n")
    print("test: get bill by id")
    total += 1
    i = db.get_bill_by_id("7070")
    if i is not None:
        print(i)
        passed += 1
    print("------------------------------------------------------------\n\n")
    updated = db.update_bill(new_bill)
    if updated is not None:
        passed += 1
    print("------------------------------------------------------------\n\n")

    print("test: delete a bill")
    total += 1
    if db.delete_bill_by_id("7070"):
        passed += 1
    print("------------------------------------------------------------\n\n")
    
    
    # write tests above this
    print(f"Total tests: {total}\nPassed: {passed}\nFailed: {total - passed}\nIf there are no errors then the tests "
          f"should have all passed yippie")
