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
            name = item.get("name")
            product_code = item.get("product_code")
            currency = item.get("currency")
            price = item.get("price")
            price_per_unit = item.get("furnished")
            ingredients = item.get("ingredients")
            nutri_score_letter = item.get("nutri_score_letter")
            description = item.get("description")
            imges_url  = item.get("imges_url")

            data = [
                    product_url,
                    name,
                    product_code,
                    currency,
                    price,
                    price_per_unit,
                    ingredients,
                    nutri_score_letter,
                    description,
                    imges_url 
            ]
            self.writer.writerow(data)


with open(file_name, "a", encoding="utf-8",newline="") as file:
        writer_file = csv.writer(file, delimiter=",")
        export = Export(writer_file)
        export.start()
        file.close()

