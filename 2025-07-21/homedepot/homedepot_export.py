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
            brand = item.get("brand", "")
            breadcrumb = item.get("breadcrumb", "")
            retail_limit = item.get("retail_limit", "")
            currency = item.get("currency", "")
            selling_price = item.get("selling_price", "")
            price_was = item.get("price_was", "")
            images = item.get("images", "")
            rating = item.get("rating", "")
            review = item.get("review", "")
            product_description = item.get("product_description", "")
            product_details = item.get("product_details", "")

            price_was = price_was if price_was != 0.0 else ""

            data = [
                 url,
                 product_name,
                 brand,
                 breadcrumb,
                 retail_limit,
                 currency,
                 selling_price,
                 price_was,
                 images,
                 rating,
                 review,
                 product_description,
                 product_details
            ]
            self.writer.writerow(data)



if __name__ == "__main__":
    with open(file_name, "a", encoding="utf-8", newline="") as file:
            writer_file = csv.writer(file, delimiter=",")
            export = Export(writer_file)
            export.start()
            file.close()
