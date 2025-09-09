import logging
import csv
import re
from settings import file_name,FILE_HEADERS, MONGO_URI, DB_NAME, PARSE_COLLECTION
from pymongo import MongoClient
from datetime import datetime


client = MongoClient(MONGO_URI)  
db = client[DB_NAME] 


class Export:
    def __init__(self,writer):
        self.writer = writer
    def start(self):
        self.writer.writerow(FILE_HEADERS)
        logging.info(FILE_HEADERS)

        for item in db[PARSE_COLLECTION].find():
            pdp_url = item.get("pdp_url", "")
            brand = item.get("brand", "")
            vendor_Seller_part_number = item.get("sku", "")
            item_name = item.get("item_name", "")
            product_description = item.get("product_description", "")
            price = item.get("price", "")
            upc = item.get("upc", "")
            model_number = item.get("model_number", "")
            product_category = item.get("product_category", "")
            date_crawled = item.get("date_crawled", "")
            
            price = f"{price:.2f}" if price != 0 else ""
            product_description = (
                re.sub(r"\s+", " ", product_description.replace("\xa0", " ")).strip()
                if product_description else ""
            )
            date_crawled = date_crawled.strftime("%Y-%m-%d")

            
            company_name = "mrosupply"
            manufacturer_name = ""
            manufacturer_part_number = ""
            country_of_origin = ""
            unit_of_issue = ""
            qty_per_uoi = ""
            availability = ""
            
            
            data =[
                company_name,
                manufacturer_name,
                brand,
                manufacturer_part_number,
                vendor_Seller_part_number,
                item_name,
                product_description,
                price,
                country_of_origin,
                unit_of_issue,
                qty_per_uoi,
                upc,
                model_number,
                product_category,
                pdp_url,
                availability,
                date_crawled
            ]
            self.writer.writerow(data)



if __name__ == "__main__":
    with open(file_name, "a", encoding="utf-8", newline="") as file:
            writer_file = csv.writer(file, delimiter=",")
            export = Export(writer_file)
            export.start()
            file.close()
