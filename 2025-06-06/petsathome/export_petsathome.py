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
            url = item.get("pdp_url")
            product_name = item.get("product_name")
            product_unique_key = item.get("product_unique_key")
            price = item.get("regular_price")
            brand = item.get("brand")
            images = item.get("images")
            rating = item.get("rating")
            review = item.get("review")
            netweight = item.get("net_weight")
            valid_upto = item.get("valid_upto")
            features = item.get("features")
            ingredients = item.get("ingredients")
            promotion_description = item.get("promotion_description")
            feeding_recommendation = item.get("feeding_recommendation")
            material_composition = item.get("material_composition")
            product_description = item.get("product_description")


            data = [
                url,
                product_name,
                product_unique_key,
                price,
                brand,
                images,
                rating,
                review,
                netweight,
                valid_upto,
                features,
                ingredients,
                promotion_description,
                feeding_recommendation,
                material_composition,
                product_description
            ]
            self.writer.writerow(data)


with open(file_name, "a", encoding="utf-8",newline="") as file:
        writer_file = csv.writer(file, delimiter=",")
        export = Export(writer_file)
        export.start()
        file.close()

