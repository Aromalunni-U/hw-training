import logging
import csv
from settings import file_name,FILE_HEADERS, MONGO_URI, DB_NAME, DATA_COLLECTION
from pymongo import MongoClient

client = MongoClient(MONGO_URI)  
db = client[DB_NAME] 


class Export:
    def __init__(self,writer):
        self.writer = writer
    def start(self):
        self.writer.writerow(FILE_HEADERS)
        logging.info(FILE_HEADERS)

        for item in db[DATA_COLLECTION].find().limit(200):
            url = item.get("pdp_url", "")
            product_id = item.get("product_id", "") 
            product_name = item.get("product_name", "") 
            brand = item.get("brand", "") 
            currency = item.get("currency", "") 
            selling_price = item.get("selling_price", "") 
            regular_price = item.get("regular_price", "") 
            promotion_description = item.get("promotion_description", "").replace("Â", "")
            review = item.get("review", "") 
            rating = item.get("rating", "") 
            image = item.get("image", "") 
            product_description = item.get("product_description", "")
            size = item.get("size", "")
            material_care = item.get("material_care", "") 
            availability = item.get("availability", "") 

            data = [
                 url,
                 product_id,
                 product_name,
                 brand,
                 currency,
                 selling_price,
                 regular_price,
                 promotion_description,
                 review,
                 rating,
                 image,
                 product_description,
                 size,
                 material_care,
                 availability
            ]
            self.writer.writerow(data)



if __name__ == "__main__":
    with open(file_name, "a", encoding="utf-8", newline="") as file:
            writer_file = csv.writer(file, delimiter=",")
            export = Export(writer_file)
            export.start()
            file.close()
