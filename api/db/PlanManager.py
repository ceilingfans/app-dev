from pymongo import MongoClient, ReturnDocument
from pymongo.database import Collection

from api.structures.PlanDescription import PlanDescription


class PlanManager:
    client: MongoClient
    col: Collection

    def __init__(self, client: MongoClient, col: Collection):
        self.client = client
        self.col = col

    def create(self, plan: PlanDescription):
        """Creates a plan

        Returns:
            | Plan Exists - ("PLANEXISTS", PlanDescription)
            | Success - ("SUCCESS", PlanDescription)
            | Error - ("ERROR", Error)
        """
        ret_code, exists = self.find(plan.get_plan_type().value)
        if ret_code == "ERROR":
            return ret_code, exists

        if exists:
            return "PLANEXISTS", exists

        try:
            self.col.insert_one(dict(plan))
            return "SUCCESS", plan

        except Exception as e:
            return "ERROR", e

    def find(self, plan_type: str = None):
        """Find a plan or read all plans in the collection

        Returns:
            | All Plans - ("ALL", List[PlanDescription])
            | Plan Not Found - ("PLANNOTFOUND", None)
            | Success - ("SUCCESS", PlanDescription)
        """
        try:
            if plan_type is None:
                return "ALL", self.col.find()

            result = self.col.find_one({"plan_type": plan_type})
            if result is None:
                return "PLANNOTFOUND", None

            return "SUCCESS", PlanDescription(result)

        except Exception as e:
            return "ERROR", e

    def update(self, plan_type: str, new_plan: dict):
        """Updates a plan with the given information,
        does not need the full plan object to update,

        Returns:
            | Plan Not Found - ("PLANNOTFOUND", None)
            | Success - ("SUCCESS", PlanDescription)
            | Error - ("Error", Error)
        """
        try:
            result = self.col.find_one_and_update({"plan_type": plan_type}, {"$set": new_plan}, return_document=ReturnDocument.AFTER)
            if result is None:
                return "PLANNOTFOUND", None

            return "SUCCESS", PlanDescription(result)

        except Exception as e:
            return "ERROR", e

    def delete(self, plan_type: str):
        """Deletes a plan

        Results:
            | Plan Not Found - ("PLANNOTFOUND", None)
            | Success: ("SUCCESS", None)
            | Error: ("ERROR", Error)
        """
        try:
            result = self.col.delete_one({"plan_type": plan_type})
            if result.deleted_count == 0:
                return "PLANNOTFOUND", None

            return "SUCCESS", None

        except Exception as e:
            return "ERROR", e