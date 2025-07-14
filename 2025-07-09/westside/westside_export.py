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
            brand = item.get("brand", "")
            net_quantity = item.get("net_quantity", "")
            country_of_origin = item.get("country_of_origin", "")
            description = item.get("description", "")
            care_instructions = item.get("care_instructions", "")
            material_composition = item.get("material_composition", "")
            clothing_fit = item.get("clothing_fit", "")
            images = item.get("images", "")     
            color = item.get("color", "")        
            breadcrumb = item.get("breadcrumb", "")
            sku = item.get("sku", "")
            size = item.get("size", "") 


            data = [
                url,
                product_name,
                regular_price,
                brand,
                net_quantity,
                country_of_origin,
                description,
                care_instructions,
                material_composition,
                clothing_fit,
                images,
                color,
                breadcrumb,
                sku,
                size
            ]

            self.writer.writerow(data)



if __name__ == "__main__":
    with open(file_name, "a", encoding="utf-8", newline="") as file:
            writer_file = csv.writer(file, delimiter=",")
            export = Export(writer_file)
            export.start()
            file.close()
