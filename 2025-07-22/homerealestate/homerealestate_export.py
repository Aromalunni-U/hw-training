from pymongo import MongoClient
import json
from settings import MONGO_URI, DB_NAME, DATA_COLLECTION


class Export:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        self.collection = self.db[DATA_COLLECTION]

    def start(self):
        documents = list(self.collection.find({}, {'_id': 0}))

        for doc in documents:

            name = doc.get("name", "")

            first_name = ""
            middle_name = ""
            last_name = ""

            if "&" not in name:
                full_name = name.strip().split()
                if len(full_name) == 2:
                    first_name = full_name[0]
                    last_name = full_name[1]
                
                elif len(full_name) == 3:
                    first_name = full_name[0]
                    middle_name = full_name[1]
                    last_name = full_name[2]
            else:
                first_name = name.strip()


            first_name = first_name.strip() 
            middle_name = middle_name.strip()
            last_name = last_name.strip()

            doc["first_name"] = first_name
            doc["middle_name"] = middle_name
            doc["last_name"] = last_name
            doc["language"] = ""
            doc["country"] = "United States"

            if "name" in doc:
                del doc["name"]
            

        with open("homerealestate.json", "w", encoding="utf-8") as f:
            json.dump(documents, f, indent=2, ensure_ascii=False)
            
if __name__ == "__main__":
    export = Export()
    export.start()