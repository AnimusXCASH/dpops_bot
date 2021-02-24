class IntegrityCheck(object):
    def __init__(self, connection):
        self.connection = connection
        self.dpops_delegate = self.connection["DpopsDelegate"]  #
        self.required_collections = ["votersDb", "botSettings"]
        self.required_documents = ["new_block", "delegate_daily"]

    def check_collections(self):
        """
        Check all required collections
        """
        # Check collections for bot stats
        bot_collections = self.dpops_delegate.list_collection_names()
        for collection in self.required_collections:
            if collection not in bot_collections:
                print(f"Collection {collection} missing... creating")
                self.dpops_delegate.create_collection(name=collection)
                print("created")

        print("Checking required documents")
        all_documents = [x["setting"] for x in self.dpops_delegate.botSettings.find({})]
        for r in self.required_documents:
            if r not in all_documents:
                # Insert required document
                data = {
                    "channel": int(0),
                    "value": int(0),
                    "setting": r,
                    "status": 0,
                }
                status = self.dpops_delegate.botSettings.insert_one(data)
                if status.inserted_id:
                    print(f"New documment created successfully: {r}")
                else:
                    print(f"ERROR: Document {r} could not be inserted into collection of botSettings")
