from pymongo import MongoClient, ReturnDocument
from pymongo.database import Collection

from api.structures.InsuredItem import InsuredItem


class ItemManager:
    client: MongoClient
    col: Collection

    def __init__(self, client: MongoClient, col: Collection):
        self.client = client
        self.col = col

    def create(self, item: InsuredItem):
        """Creates an insured item

        Returns:
            | Item Exists - ("ITEMEXISTS", InsuredItem)
            | Success - ("SUCCESS", InsuredItem)
            | Error - ("ERROR", Error)
        """

    def find(self, owner_id: str = None, item_id: str = None):
        """Finds an insured by item id, all items belonging to an owner or all items in the collection

        Returns:
            | All Items - ("ALL", List[InsuredItem])
            | Owner Items - ("OWNERITEMS", List[InsuredItem])
            | Success - ("SUCCESS", InsuredItem)
            | Error - ("ERROR", Error)
        """
        try:
            if owner_id is None and item_id is None:
                return "ALL", self.col.find()

            if owner_id is not None:
                return "OWNERITEMS", InsuredItem(self.col.find_({"owner_id": owner_id}))

            if item_id is not None:
                return "SUCCESS", InsuredItem(self.col.find_one({"item_id": item_id}))

        except Exception as e:
            return "ERROR", e

    def update(self, item_filter: dict, new_item: dict):
        """Updates an item with the given information, does not need the full item object,
         `item_filter` is to allow updating with different things

         Returns:
            | Item Not Found - ("ITEMNOTFOUND", None)
            | Success - ("SUCCESS", User)
            | Error - ("Error", Error)
        """
        try:
            result = self.col.find_one_and_update(item_filter, {"$set": new_item}, return_document=ReturnDocument.AFTER)
            if result is None:
                return "ITEMNOTFOUND", None

            return "SUCCESS", InsuredItem(result)

        except Exception as e:
            return "ERROR", e

    def delete(self, item_id: str):
        """Deletes an item, uses `item_id` as the user needs to be logged in to delete the item

        Results:
            | Item Not Found - ("ITEMNOTFOUND", None)
            | Success: ("SUCCESS", None)
            | Error: ("ERROR", Error)
        """
        try:
            result = self.col.delete_one({"_id": item_id})
            if result.deleted_count == 0:
                return "ITEMNOTFOUND", None

            return "SUCCESS", None

        except Exception as e:
            return "ERROR", e
