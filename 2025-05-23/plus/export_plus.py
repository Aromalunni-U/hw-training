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
            product_url = item.get("product_url")
            name = item.get("product_name")
            price = item.get("product_price")
            ingredients = item.get("product_ingredients")
            nutrients = item.get("product_nutrients")
            base_unit_price = item.get("product_base_unit_price")
            breadcrumb = item.get("breadcrumb")
            imges_url  = item.get("product_image")

            data = [
                    product_url,
                    name,
                    price,
                    ingredients,
                    nutrients,
                    base_unit_price,
                    breadcrumb,
                    imges_url
            ]
            self.writer.writerow(data)


with open(file_name, "a", encoding="utf-8",newline="") as file:
        writer_file = csv.writer(file, delimiter=",")
        export = Export(writer_file)
        export.start()
        file.close()

