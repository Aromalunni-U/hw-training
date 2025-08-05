import logging
import csv
import re
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
            unique_id = item.get("unique_id", "")
            product_name = item.get("product_name", "")
            regular_price = item.get("regular_price", "")
            selling_price = item.get("selling_price", "")
            percentage_discount = item.get("percentage_discount", "")
            breadcrumb = item.get("breadcrumb", "")
            pdp_url = item.get("pdp_url", "")

            breadcrumb = f"Főoldal > Online áruház > {breadcrumb} > {product_name}"
            percentage_discount = percentage_discount if percentage_discount != 0 else ""
            regular_price = regular_price if regular_price != selling_price else ""

            pattern = r'\d+\s*(g|kg|ml|l)'
            match = re.findall(pattern, product_name.lower())
            uom = match[-1] if match else ""

            if match:
                uom = match[-1].strip()
            else:
                uom = ""

            data= [
                 unique_id,
                 product_name,
                 regular_price,
                 selling_price,
                 percentage_discount,
                 breadcrumb,
                 pdp_url,
                 uom
             ]

            self.writer.writerow(data)

if __name__ == "__main__":
    with open(file_name, "a", encoding="utf-8", newline="") as file:
            writer_file = csv.writer(file, delimiter=",")
            export = Export(writer_file)
            export.start()
            file.close()
