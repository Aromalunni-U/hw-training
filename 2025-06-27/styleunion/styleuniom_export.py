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
            color = item.get("color", "")
            sku = item.get("sku", "")
            size = item.get("size", "")
            care_instructions = item.get("care_instructions", "")
            fabric_type = item.get("fabric_type", "")
            rating = item.get("rating", "")
            review = item.get("review", "")
            pattern = item.get("pattern", "")
            pocket = item.get("pocket", "")
            clothing_fit = item.get("clothing_fit", "")
            sleeve_type = item.get("sleeve_type", "")
            collar_type = item.get("collar_type", "")
            clothing_length = item.get("clothing_length", "")
            product_description = item.get("product_description", "")
            images = item.get("images", "")

            data = [
                url,
                product_name,
                regular_price,
                color,
                sku,
                size,
                care_instructions,
                fabric_type,
                rating,
                review,
                pattern,
                pocket,
                clothing_fit,
                sleeve_type,
                collar_type,
                clothing_length,
                product_description,
                images
            ]
            self.writer.writerow(data)



if __name__ == "__main__":
    with open(file_name, "a", encoding="utf-8",newline="") as file:
            writer_file = csv.writer(file, delimiter=",")
            export = Export(writer_file)
            export.start()
            file.close()
