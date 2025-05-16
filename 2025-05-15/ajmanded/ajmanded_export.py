import logging
import csv
from settings import *
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
            real_estate_link = item.get("real_estate_link")
            license_number = item.get("license_number")
            license_type = item.get("license_type")
            legal_form = item.get("legal_form")
            arabic_trade_name = item.get("arabic_trade_name")
            english_trade_name = item.get("english_trade_name")
            license_start_date = item.get("license_start_date")
            license_expiry_date = item.get("license_expiry_date")
            activities = item.get("activities")
            est_banning_status= item.get("est_banning_status")
            area = item.get("area")

            data = [
                real_estate_link,
                license_number,
                license_type,
                legal_form,
                arabic_trade_name,
                english_trade_name,
                license_start_date,
                license_expiry_date,
                activities,
                est_banning_status,
                area
            ]
            self.writer.writerow(data)


with open(file_name, "a", encoding="utf-8",newline="") as file:
        writer_file = csv.writer(file, delimiter=",")
        export = Export(writer_file)
        export.start()
        file.close()