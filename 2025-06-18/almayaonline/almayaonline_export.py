import logging
import csv
from settings import file_name,FILE_HEADERS, MONGO_URI, DB_NAME, PARSE_COLLECTION
from pymongo import MongoClient

client = MongoClient(MONGO_URI)  
db = client[DB_NAME] 


class Export:
    def __init__(self,writer):
        self.writer = writer
    def start(self):
        self.writer.writerow(FILE_HEADERS)
        logging.info(FILE_HEADERS)

        for item in db[PARSE_COLLECTION].find():
            url = item.get("pdp_url", "")
            product_name = item.get("product_name", "")
            unique_id = item.get("unique_id", "")
            currency = item.get("currency", "")
            regular_price = item.get("regular_price", "")
            images = item.get("images", "")
            product_description = item.get("product_description", "") 

            data = [
                 url,
                 product_name,
                 unique_id,
                 currency,
                 regular_price,
                 images,
                 product_description
            ]
            self.writer.writerow(data)



if __name__ == "__main__":
    with open(file_name, "a", encoding="utf-8",newline="") as file:
            writer_file = csv.writer(file, delimiter=",")
            export = Export(writer_file)
            export.start()
            file.close()

