from pymongo import MongoClient, ReturnDocument
from pymongo.database import Collection

from api.structures.Promo import Promo


class PromoManager:
    client: MongoClient  # not sure if we need this but have it in case
    col: Collection

    def __init__(self, client: MongoClient, col: Collection):
        self.client = client
        self.col = col

    def create(self, promo: Promo):
        """Create a promo

        Returns:
            | Promo Exists - ("PROMOEXISTS", Promo)
            | Success - ("SUCCESS", Promo)
            | Error - ("ERROR", None)
        """
        ret_code, exists = self.find(promo.get_id())
        if ret_code == "ERROR":
            return ret_code, exists

        if exists:
            return "USEREXISTS", exists

        try:
            self.col.insert_one(dict(promo))

        except Exception as e:
            return "ERROR", e

    def find(self, promo_id: str = None):
        """Find a promo or read all promos in the collection

        Returns:
            | All Promos - ("ALL", List[Promo])
            | Promo Not Found - ("PROMONOTFOUND, None)
            | Success - ("SUCCESS", Promo)
            | Error - ("ERROR", Error)
        """
        try:
            if promo_id is None:
                return "ALL", self.col.find()

            return "SUCCESS", self.col.find_one({"id": promo_id})

        except Exception as e:
            return "ERROR", e

    def update(self, promo_id: str, new_promo: dict):
        """Updates a promo with the given information, only has `promo_id` as a filter

        Returns:
            | Promo Not Found - ("PROMONOTFOUND", None)
            | Success - ("SUCCESS", Promo)
            | Error - ("ERROR", Error)
        """
        try:
            result = self.col.find_one_and_update({"id": promo_id}, {"$set": new_promo}, return_document=ReturnDocument.AFTER)
            if result is None:
                return "PROMONOTFOUND", None

            return "SUCCESS", Promo(result)

        except Exception as e:
            return "ERROR", e

    def delete(self, promo_id: str):
        """Delete a promo

        Returns:
            | Promo Not Found - ("PROMONOTFOUND", None)
            | Success - ("SUCCESS", None)
            | Error - ("ERROR", Error)
        """
        try:
            result = self.col.delete_one({"id": promo_id})
            if result.deleted_count == 0:
                return "PROMONOTFOUND", None

            return "SUCCESS", None

        except Exception as e:
            return "ERROR", e
