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

    def find(self, bill_id: str = None, owner_id: str = None):
        """Find a bill or read all bills in the collection

        Returns:
            | All Bills - ("ALL", List[Bill])
            | Bill Not Found - ("BILLNOTFOUND", None)
            | Owner Bills - ("OWNERBILLS", List[Bill])
            | Success - ("SUCCESS", Bill)
        """
        try:
            if bill_id is None and bill_id is None:
                return "ALL", self.col.find()

            query = {}
            owner_flag = False

            if bill_id is not None:
                query = {"bill_id": bill_id}
            elif owner_id is not None:
                query = {"owner_id": owner_id}

            result = list(self.col.find(query))
            if len(result) == 0:
                return "BILLNOTFOUND", None

            if not owner_flag:
                return "SUCCESS", Bill(result[0])

            return "OWNERBILLS", [Bill(bill) for bill in result]

        except Exception as e:
            return "ERROR", e

    def update(self, bill_id: str, new_bill: dict):
        """Updates a bill with the given information, does not need the full bill object to update

        Returns:
            | Bill Not Found - ("BILLNOTFOUND", None)
            | Success - ("SUCCESS", Bill)
        """
        try:
            result = self.col.find_one_and_update({"bill_id": bill_id}, {"$set": new_bill}, return_document=ReturnDocument.AFTER)
            if result is None:
                return "BILLNOTFOUND", None

            return "SUCCESS", Bill(result)

        except Exception as e:
            return "ERROR", e

    def delete(self, bill_id: str):
        """Deletes a bill

        Results:
            | Bill Not Found - ("BILLNOTFOUND", None)
            | Success: ("SUCCESS", None)
            | Error: ("ERROR", Error)
        """
        try:
            result = self.col.delete_one({"bill_id": bill_id})
            if result.deleted_count == 0:
                return "BILLNOTFOUND", None

            return "SUCCESS", None

        except Exception as e:
            return "ERROR", e