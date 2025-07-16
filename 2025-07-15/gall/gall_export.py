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
            regular_price = item.get("regular_price", "")
            price_was = item.get("price_was", "")
            percentage_discount = item.get("percentage_discount", "")
            product_description = item.get("product_description", "")
            breadcrumb = item.get("breadcrumb", "")
            rating = item.get("rating", "")
            review = item.get("review", "")
            image = item.get("image", "")
            alchole_percentage = item.get("alchole_percentage", "")
            ingredient = item.get("ingredient", "")
            allergens = item.get("allergens", "")
            alchol_by_volume = item.get("alchol_by_volume", "")
            instock = item.get("instock", "")
            nutritions = item.get("nutritions", "")

            data = [
                 url,
                 product_name,
                 regular_price,
                 price_was,
                 percentage_discount,
                 product_description,
                 breadcrumb,
                 rating,
                 review,
                 image,
                 alchole_percentage,
                 ingredient,
                 allergens,
                 alchol_by_volume,
                 instock,
                 nutritions
            ]

            self.writer.writerow(data)



if __name__ == "__main__":
    with open(file_name, "a", encoding="utf-8", newline="") as file:
            writer_file = csv.writer(file, delimiter=",")
            export = Export(writer_file)
            export.start()
            file.close()
