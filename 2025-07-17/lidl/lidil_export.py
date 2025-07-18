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
            price_was = item.get("price_was", "")
            percentage_discount = item.get("percentage_discount", "")
            selling_price = item.get("selling_price", "")
            images = item.get("images", "")
            review = item.get("review", "")
            rating = item.get("rating", "")
            breadcrumb = item.get("breadcrumb", "")
            brand = item.get("brand", "")
            size = item.get("size", [])
            care_instructions = item.get("care_instructions", "")
            properties = item.get("properties", "")
            features = item.get("features", {})


            price_was = "" if price_was == 0.0 else price_was
            size = size if size else ""
            features = features if features else ""

            data = [
                 url,
                 product_name,
                 price_was,
                 percentage_discount,
                 selling_price,
                 images,
                 review,
                 rating,
                 breadcrumb,
                 brand,
                 size,
                 care_instructions,
                 properties,
                 features
            ]
            self.writer.writerow(data)



if __name__ == "__main__":
    with open(file_name, "a", encoding="utf-8", newline="") as file:
            writer_file = csv.writer(file, delimiter=",")
            export = Export(writer_file)
            export.start()
            file.close()
