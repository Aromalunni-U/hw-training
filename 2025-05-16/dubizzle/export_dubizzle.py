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
            url = item.get("link")
            currency = item.get("currency")
            price = item.get("price")
            beadroom = item.get("beadroom")
            bathroom = item.get("bathroom")
            furnished = item.get("furnished")
            area = item.get("area")
            location = item.get("location")
            amenities = item.get("amenities")
            price_type = item.get("price_type")
            breadcrumb = item.get("breadcrumb")
            description = item.get("description")
            images = item.get("images")

            data = [
                    url,
                    currency,
                    price,
                    beadroom,
                    bathroom,
                    furnished,
                    area,
                    location,
                    amenities,
                    price_type,
                    breadcrumb,
                    description,
                    images,
            ]
            self.writer.writerow(data)


with open(file_name, "a", encoding="utf-8",newline="") as file:
        writer_file = csv.writer(file, delimiter=",")
        export = Export(writer_file)
        export.start()
        file.close()

