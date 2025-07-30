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

        for item in db[PARSE_COLLECTION].find().limit(200):
            url = item.get("pdp_url", "")
            product_name = item.get("product_name", "")
            product_id = item.get("product_id", "")
            product_name = item.get("product_name", "")
            product_color = item.get("product_color", "")
            material = item.get("material", "")
            details = item.get("details", "")
            specification = item.get("specification", "")
            price = item.get("price", "")
            price_was = item.get("price_was", "")
            breadcrumb = item.get("breadcrumb", "")
            stock = item.get("stock", "")
            image = item.get("image", "")
            competitor_name = "homecentre"

            material = material if material else ""
            specification = specification if specification else ""


            data = [
                 url,
                 competitor_name,
                 product_name,
                 product_id,
                 product_color,
                 material,
                 details,
                 specification,
                 price,
                 price_was,
                 breadcrumb,
                 stock,
                 image
            ]
            self.writer.writerow(data)



if __name__ == "__main__":
    with open(file_name, "a", encoding="utf-8", newline="") as file:
            writer_file = csv.writer(file, delimiter=",")
            export = Export(writer_file)
            export.start()
            file.close()
