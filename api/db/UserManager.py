from pymongo import MongoClient, ReturnDocument
from pymongo.database import Collection

from api.structures.User import User


class UserManager:
    client: MongoClient  # not sure if we need this but have it in case
    col: Collection

    def __init__(self, client: MongoClient, col: Collection):
        self.client = client
        self.col = col

    def create(self, user: User):
        """Creates a user

        Returns:
            | User Exists - ("USEREXISTS", User)
            | Success - ("SUCCESS", User)
            | Error - ("ERROR", Error)
        """
        # will use user_id by default as there should not be dupes due to this check
        ret_code, exists = self.find(user_id=user.get_id())
        if ret_code == "ERROR":
            return ret_code, exists

        if exists:
            return "USEREXISTS", exists

        try:
            self.col.insert_one(dict(user))
            return "SUCCESS", user

        except Exception as e:
            return "ERROR", e

    def find(self, user_id: str = None, email: str = None):
        """Find a user or read all users in the collection

        Returns:
            | All Users - ("ALL", List[User])
            | User Not Found - ("USERNOTFOUND", None)
            | Success - ("SUCCESS", User)
            | Error - ("ERROR", Error)
        """
        try:
            if user_id is None and email is None:
                return "ALL", self.col.find()

            query = {}
            if user_id is not None:
                query = {"id": user_id}
            elif email is not None:
                query = {"email": email}

            result = self.col.find_one(query)
            if result is None:
                return "USERNOTFOUND", None

            return "SUCCESS", User(result)

        except Exception as e:
            return "ERROR", e

    def update(self, user_filter: dict, new_user: dict):
        """Updates a user with the given information, does not need the full user object to update, `user_filter` is to
        allow updating users using their ids or emails

        Returns:
            | User Not Found - ("USERNOTFOUND", None)
            | Success - ("SUCCESS", User)
            | Error - ("Error", Error)
        """
        try:
            result = self.col.find_one_and_update(user_filter, {"$set": new_user}, return_document=ReturnDocument.AFTER)
            if result is None:
                return "USERNOTFOUND", None

            return "SUCCESS", User(result)

        except Exception as e:
            return "ERROR", e

    def delete(self, user_id: str):
        """Deletes a user, uses `user_id` as the user must already be logged in to
        delete the account which means we have access to their id already

        Returns:
            | User Not Found - ("USERNOTFOUND", None)
            | Success: ("SUCCESS", None)
            | Error: ("ERROR", Error)
        """
        try:
            result = self.col.delete_one({"id": user_id})
            if result.deleted_count == 0:
                return "USERNOTFOUND", None

            return "SUCCESS", None

        except Exception as e:
            return "ERROR", e
