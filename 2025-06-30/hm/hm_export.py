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
            art_number = item.get("art_number", "")
            material_composition = item.get("material_composition", "")
            clothing_length = item.get("clothing_length", "")
            clothing_fit = item.get("clothing_fit", "")
            country_of_origin = item.get("country_of_origin", "")
            neck_style = item.get("neck_style", "")
            style = item.get("style", "")
            care_instruction = item.get("care_instruction", "")
            color = item.get("color", "")
            sleeve_length_style = item.get("sleeve_length_style", "")
            images = item.get("images", "")

            data = [
                url,
                product_name,
                regular_price,
                art_number,
                material_composition,
                clothing_length,
                clothing_fit,
                country_of_origin,
                neck_style,
                style,
                care_instruction,
                color,
                sleeve_length_style,
                images
            ]

            self.writer.writerow(data)



if __name__ == "__main__":
    with open(file_name, "a", encoding="utf-8",newline="") as file:
            writer_file = csv.writer(file, delimiter=",")
            export = Export(writer_file)
            export.start()
            file.close()
