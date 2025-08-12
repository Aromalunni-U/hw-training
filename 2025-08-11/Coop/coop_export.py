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
            product_id = item.get("product_id", "")
            review = item.get("review", "")
            rating = item.get("rating", "")
            breadcrumb = item.get("breadcrumb", "")
            brand = item.get("brand", "")
            selling_price = item.get("selling_price", "")
            regular_price = item.get("regular_price", "")
            grammage_quantity = item.get("grammage_quantity", "")
            grammage_unit = item.get("grammage_unit", "")
            percentage_discount = item.get("percentage_discount", "")
            country_of_origin = item.get("country_of_origin", "")
            image = item.get("image","")

            regular_price = f"{regular_price:.2f}" if regular_price != 0 else  ""
            selling_price = f"{selling_price:.2f}"
            image = image.split("?")[0].replace("310_310", "1474_1474")

            grammage_quantity = (
                 grammage_quantity if "2x" not in grammage_quantity 
                 else float(grammage_quantity.replace("2x", "").strip()) * 2
            )
            grammage_unit = grammage_unit if grammage_unit != "PCE" else "ST"
            breadcrumb = f"{breadcrumb} > {product_name}"


            data=[
                url,
                product_name,
                product_id ,
                review,
                rating,
                breadcrumb, 
                brand,
                selling_price,
                regular_price,
                grammage_quantity,
                grammage_unit,
                percentage_discount,
                country_of_origin,
                image
            ]
            self.writer.writerow(data)



if __name__ == "__main__":
    with open(file_name, "a", encoding="utf-8", newline="") as file:
            writer_file = csv.writer(file, delimiter=",")
            export = Export(writer_file)
            export.start()
            file.close()
