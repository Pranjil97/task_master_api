from pymongo import MongoClient

import uuid 
from datetime import datetime

class Mongo:
    def __init__(self, connection_string) -> None:

        self.connection_string = connection_string
        # connecting mongo db
        self.connection = MongoClient(self.connection_string)
        self.main_db = self.connection["main_db"]
        self.main_collection = self.main_db["main_collection"]
        if self.main_collection in self.main_db.list_collection_names() == False:
                self.main_collection.create_collection("main_collection")
    

    def create(self, data) -> bool :
        try:
            if isinstance(data,dict):
                data["record_id"] = uuid.uuid4().hex
                data["date"] = datetime.now()
                self.main_collection.insert_one(data)
                return True
            else:
                return False
        except Exception as e:
            print(f"FileSystemOps :: create_file :: {e}")
            return False

    def delete(self,task_id) -> bool|None:
        try:
            if self.main_collection.find_one({"record_id":task_id}):
                self.main_collection.delete_one({"record_id":task_id})
                return True
            return False
        except Exception as e:
            print(f"FileSystemOps :: delete_file :: {task_id} :: {e}")
            return False

    def update(self,task_id, data ) -> bool | None:
        try:
            if self.main_collection.find_one({"record_id":task_id}) == False:
                return None
            return self.main_collection.update_one({"record_id":task_id},{'$set':data})
        except Exception as e:
            return False

    def record(self,task_id):
        try:
            if self.main_collection.find_one({"record":task_id})==False:
                return None
            return ([i for i in self.main_collection.find({"record_id":task_id},{"_id":False})])
        except Exception as e:
            print(f"FileSystemOps :: record :: {e}")
            return None

    def list(self):
        try:
            return ([i for i in self.main_collection.find({},{"_id":False})])
        except Exception as e:
            print(f"FileSystemOps :: list_files :: {e}")
            return []