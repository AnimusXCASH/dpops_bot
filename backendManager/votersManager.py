class VotersManager:
    """
    Class to manager voters who applied for monitoring
    """

    def __init__(self, connection):
        self.connection = connection
        self.dpops_delegate = self.connection['DpopsDelegate']
        self.voters_collection = self.dpops_delegate.votersDb

    def register_voter(self, user_id: int, public_key: str):
        status = self.voters_collection.insert_one({"userId": int(user_id),
                                                    "publicKey": public_key})
        return status.inserted_id

    def check_voter(self, user_id: int):
        status = self.voters_collection.find_one({"userId": int(user_id)})
        if status:
            return True
        else:
            return False

    def update_voting_address(self, user_id: int, public_key: str):
        result = self.voters_collection.update_one({"userId": int(user_id)},
                                                   {"$set": {"publicKey": public_key}})

        return result.modified_count > 0

    def remove_voter(self, user_id: int):
        result = self.voters_collection.delete_one({"userId": int(user_id)})

        return result.deleted_count > 0

    def get_voter(self, user_id: int):
        result = self.voters_collection.find_one({"userId": int(user_id)})
        return result

    def update_payment_notification_status(self, user_id: int, status: int, timestamp: int):
        result = self.voters_collection.update_one({"userId": int(user_id)},
                                                   {"$set": {"paymentNotifications": int(status),
                                                             "lastProcessed": int(timestamp)}})
        return result.modified_count > 0

    def payment_notifications_applied(self):
        result = list(self.voters_collection.find({"paymentNotifications":{"$gt":0}}))

        return result
