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
            pdp_url = item.get("pdp_url")
            product_name = item.get("product_name")
            product_code = item.get("product_code")
            product_price = item.get("product_price") 
            currency = item.get("currency")
            brand = item.get("brand")
            images = item.get("images")
            breadcrumb = item.get("breadcrumb")
            rating = item.get("rating")
            review = item.get("review")
            features = item.get("features")
            product_description = item.get("product_description")
            ingredients = item.get("ingredients")
            storage_instructions = item.get("storage_instructions")
            warning = item.get("warning")
            company_address = item.get("company_address")
            nutritional_information = item.get("nutritional_information")
            manufacturer_address = item.get("manufacturer_address")
            promotion_valid_from = item.get("promotion_valid_from")
            promotion_valid_upto= item.get("promotion_valid_upto")
            promotion_description= item.get("promotion_description")
            percentage_discount= item.get("percentage_discount")

            data = [
                pdp_url,
                product_name,
                product_code,
                product_price, 
                currency,
                brand,
                images,
                breadcrumb,
                rating,
                review,
                features,
                product_description,
                ingredients,
                storage_instructions,
                warning,
                company_address,
                nutritional_information,
                manufacturer_address,
                promotion_valid_from,
                promotion_valid_upto,
                promotion_description,
                percentage_discount
            ]
            self.writer.writerow(data)


with open(file_name, "a", encoding="utf-8",newline="") as file:
        writer_file = csv.writer(file, delimiter=",")
        export = Export(writer_file)
        export.start()
        file.close()
