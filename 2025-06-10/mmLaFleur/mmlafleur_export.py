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
            product_sku = item.get("product_sku")
            original_price = item.get("original_price")
            sales_price = item.get("sales_price")
            category = item.get("category")
            brand = item.get("brand")
            total_number_of_reviews = item.get("total_number_of_reviews")
            star_1 = item.get("star_1")
            star_2 = item.get("star_2")
            star_3 = item.get("star_3")
            star_4 = item.get("star_4")
            star_5 = item.get("star_5")
            review_text= item.get("review_text")


            data = [
                    url,
                    product_name,
                    product_sku,
                    original_price,
                    sales_price,
                    category,
                    brand,
                    total_number_of_reviews,
                    star_1,
                    star_2,
                    star_3,
                    star_4,
                    star_5,
                    review_text,
            ]
            self.writer.writerow(data)


with open(file_name, "a", encoding="utf-8",newline="") as file:
        writer_file = csv.writer(file, delimiter=",")
        export = Export(writer_file)
        export.start()
        file.close()

