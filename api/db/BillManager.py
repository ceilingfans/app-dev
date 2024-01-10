from pymongo import MongoClient, ReturnDocument
from pymongo.database import Collection

from api.structures.Bill import Bill


class BillManager:
    client: MongoClient
    col: Collection

    def __init__(self, client: MongoClient, col: Collection):
        self.client = client
        self.col = col

    def create(self, bill: Bill):
        """Creates a bill

        Returns:
            | Bill Exists - ("BILLEXISTS", Bill)
            | Success - ("SUCCESS", Bill)
            | Error - ("ERROR", Error)
        """
        ret_code, exists = self.find(bill.get_bill_id())
        if ret_code == "ERROR":
            return ret_code, exists

        if exists:
            return "BILLEXISTS", exists

        try:
            self.col.insert_one(dict(bill))
            return "SUCCESS", bill

        except Exception as e:
            return "ERROR", e

    def find(self, bill_id: str = None):
        """Find a bill or read all bills in the collection

        Returns:
            | All Bills - ("ALL", List[Bill])
            | Bill Not Found - ("BILLNOTFOUND", None)
            | Success - ("SUCCESS", Bill)
        """
        try:
            if bill_id is None:
                return "ALL", self.col.find()

            return "SUCCESS", Bill(self.col.find_one({"id": bill_id}))

        except Exception as e:
            return "ERROR", e

    def update(self, bill_id: str, new_bill: dict):
        """Updates a bill with the given information, does not need the full bill object to update

        Returns:
            | Bill Not Found - ("BILLNOTFOUND", None)
            | Success - ("SUCCESS", Bill)
        """
        try:
            result = self.col.find_one_and_update({"id": bill_id}, {"$set": new_bill}, return_document=ReturnDocument.AFTER)
            if result is None:
                return "BILLNOTFOUND", None

            return "SUCCESS", Bill(result)

        except Exception as e:
            return "ERROR", e