from pymongo import MongoClient
from pymongo.database import Database
from pymongo.server_api import ServerApi
from dotenv import load_dotenv, find_dotenv
import os
import uuid
import sys

#TODO: 
#sys.path.append("C://Users//mdame//app-dev")

from api.db.UserManager import UserManager
from api.db.PromoManager import PromoManager
from api.db.ItemManager import ItemManager
from api.db.PlanManager import PlanManager
from api.db.BillManager import BillManager

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
    promos: PromoManager
    items: ItemManager
    plans: PlanManager
    bills: BillManager

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


# test code, please ignore
if __name__ == "__main__":
    import datetime
    from api.structures.User import User, get_hash
    from api.structures.Promo import Promo
    from api.structures.PlanDescription import PlanDescription
    from api.structures.InsuredItem import InsuredItem
    from api.structures.Bill import Bill

    db = Driver()
    current = datetime.datetime.now()

    def _test(desc):
        global current

        print(f"test: {desc}")
        current = datetime.datetime.now()


    def _pass():
        print(f"passed in {(datetime.datetime.now() - current).total_seconds()}s\n")


    # user vars
    user_id = "e3e7234f-3933-483d-8a8d-7b7a9eb33b80-TEST-DO-NOT-USE"

    """
    User Tests
    """
    # create user
    _test("create user")
    user = User({
        "name": "John Doe",
        "password": get_hash("password"),
        "id": user_id,
        "email": "test@test.com",
        "address": "1234 Test St",
    })
    ret_code, user = db.users.create(user)

    assert ret_code == "SUCCESS", f"expected to create a user, got {ret_code} with error {str(user)}"
    _pass()

    # find user
    _test("find user")
    ret_code, user = db.users.find(user_id)

    assert ret_code == "SUCCESS", f"expected to find a user, got {ret_code} with error {str(user)}"
    _pass()

    # update user
    _test("update user")
    ret_code, user = db.users.update({"id": user_id}, {"name": "Jane Doe"})

    assert ret_code == "SUCCESS", f"expected to update a user, got {ret_code} with error {str(user)}"
    assert user.get_name() == "Jane Doe", f"expected user name to be Jane Doe, got {user.get_name()}"
    _pass()

    # delete user
    _test("delete user")
    ret_code, err = db.users.delete(user_id)

    assert ret_code == "SUCCESS", f"expected to delete a user, got {ret_code} with error {str(err)}"
    _pass()

    """
    Promo Tests
    """
    # promo vars
    promo_id = "XMAS10-TEST-DO-NOT-USE"

    # create promo
    _test("create promo")
    promo = Promo({
        "id": promo_id,
        "type": "Percentage",
        "value": 10,
        "expire": 1704889739058
    })
    ret_code, promo = db.promos.create(promo)

    assert ret_code == "SUCCESS", f"expected to create a promo, got {ret_code} with error {str(promo)}"
    _pass()

    # find promo
    _test("find promo")
    ret_code, promo = db.promos.find(promo_id)

    assert ret_code == "SUCCESS", f"expected to find a promo, got {ret_code} with error {str(promo)}"
    _pass()

    # update promo
    _test("update promo")
    ret_code, promo = db.promos.update(promo_id, {"type": "Value"})

    assert ret_code == "SUCCESS", f"expected to update a promo, got {ret_code} with error {str(promo)}"
    assert promo.get_type().name == "Value", f"expected promo type to be Value, got {promo.get_type()}"
    _pass()

    # delete promo
    _test("delete promo")
    ret_code, err = db.promos.delete(promo_id)

    assert ret_code == "SUCCESS", f"expected to delete a promo, got {ret_code} with error {str(err)}"
    _pass()

    """
    Plan Tests
    """
    # plan vars
    plan_type = "Bronze"  # TODO: use actual plan types

    # create plan
    _test("create plan")
    plan = PlanDescription({
        "plan_type": plan_type,
        "description": "Bronze covers the basics",
        "mean_cost": 25.75
    })
    ret_code, plan = db.plans.create(plan)

    assert ret_code == "SUCCESS", f"expected to create a plan, got {ret_code} with error {str(plan)}"
    _pass()

    # find plan
    _test("find plan")
    ret_code, plan = db.plans.find(plan_type)

    assert ret_code == "SUCCESS", f"expected to find a plan, got {ret_code} with error {str(plan)}"
    _pass()

    # update plan
    _test("update plan")
    ret_code, plan = db.plans.update(plan_type, {"description": "Bronze covers the basics and more"})

    assert ret_code == "SUCCESS", f"expected to update a plan, got {ret_code} with error {str(plan)}"
    assert plan.get_description() == "Bronze covers the basics and more", f"expected plan description to be Bronze covers the basics and more, got {plan.get_description()}"
    _pass()

    # delete plan
    _test("delete plan")
    ret_code, err = db.plans.delete(plan_type)

    assert ret_code == "SUCCESS", f"expected to delete a plan, got {ret_code} with error {str(err)}"
    _pass()

    """
    Item Tests
    """
    # item vars
    item_id = "202a334f-f5a9-464b-813e-2c94c4e83906-TEST-DO-NOT-USE"

    # create item
    _test("create item")
    item = InsuredItem({
        "owner_id": user_id,
        "item_id": item_id,
        "status": {
            "damage": {
                "description": "I dropped my phone :cat_cry:",
                "date": 1704889739058
            },
            "repair_status": {
                "past_repairs": [
                    {
                        "description": "Replaced the battery",
                        "start_date": 1704889739058,
                        "end_date": 1704889739058
                    }
                ],
                "current": {
                    "description": "Replace the screen",
                    "start_date": 1704889739058,
                    "end_date": None
                }
            },
            "address": "1234 Test St"
        },
        "subscription": {
            "plan": "Bronze",
            "duration": {
                "start_date": 1704889739058,
                "end_date": 1704889839058,
                "length": 100000
            }
        }
    })
    ret_code, item = db.items.create(item)

    assert ret_code == "SUCCESS", f"expected to create an item, got {ret_code} with error {str(item)}"
    _pass()

    # find item
    _test("find item")
    ret_code, item = db.items.find(item_id=item_id)

    assert ret_code == "SUCCESS", f"expected to find an item, got {ret_code} with error {str(item)}"
    _pass()

    # update item
    _test("update item")
    ret_code, item = db.items.update({"item_id": item_id}, {"status.address": "12345 Test St"})

    assert ret_code == "SUCCESS", f"expected to update an item, got {ret_code} with error {str(item)}"
    assert item.get_status().get_address() == "12345 Test St", f"expected item address to be 12345 Test St, got {item.get_status().get_address()}"
    _pass()

    # delete item
    _test("delete item")
    ret_code, err = db.items.delete(item_id)

    assert ret_code == "SUCCESS", f"expected to delete an item, got {ret_code} with error {str(err)}"
    _pass()

    """
    Bill Tests
    """
    # bill vars
    bill_id = "29b7d25c-aa87-4ead-9be2-f8d0646d21c2-TEST-DO-NOT-USE"

    # create bill
    _test("create bill")
    bill = Bill({
        "customer_id": user_id,
        "bill_id": bill_id,
        "status": False
    })
    ret_code, bill = db.bills.create(bill)

    assert ret_code == "SUCCESS", f"expected to create a bill, got {ret_code} with error {str(bill)}"
    _pass()

    # find bill
    _test("find bill")
    ret_code, bill = db.bills.find(bill_id=bill_id)

    assert ret_code == "SUCCESS", f"expected to find a bill, got {ret_code} with error {str(bill)}"
    _pass()

    # update bill
    _test("update bill")
    ret_code, bill = db.bills.update(bill_id, {"status": True})

    assert ret_code == "SUCCESS", f"expected to update a bill, got {ret_code} with error {str(bill)}"
    assert bill.get_status(), f"expected bill status to be True, got {bill.get_status()}"
    _pass()

    # delete bill
    _test("delete bill")
    ret_code, err = db.bills.delete(bill_id)

    assert ret_code == "SUCCESS", f"expected to delete a bill, got {ret_code} with error {str(err)}"
    _pass()
