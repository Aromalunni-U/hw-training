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
            product_id = item.get("product_id", "")
            product_name = item.get("product_name", "")
            brand = item.get("brand", "")
            selling_price = item.get("selling_price", "")
            price_was = item.get("price_was", "")
            currency = item.get("currency", "")
            rating = item.get("rating", "")
            review = item.get("review", "")
            image = item.get("image", "")
            instock = item.get("instock", "")
            breadcrumb = item.get("breadcrumb", "")
            promotion_description = item.get("promotion_description", "") 
            product_description = item.get("product_description", "")

            price_was = price_was if price_was != 0.0 else ""
            product_id = product_id.split("-")[-1]

            data = [
                 url,
                 product_id,
                 product_name,
                 brand,
                 selling_price,
                 price_was,
                 currency,
                 rating,
                 review,
                 image,
                 instock,
                 breadcrumb,
                 promotion_description,
                 product_description
            ]

            self.writer.writerow(data)

if __name__ == "__main__":
    with open(file_name, "a", encoding="utf-8", newline="") as file:
            writer_file = csv.writer(file, delimiter=",")
            export = Export(writer_file)
            export.start()
            file.close()
