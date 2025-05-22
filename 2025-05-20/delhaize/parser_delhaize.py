import requests
import logging
from pymongo import MongoClient
from settings import MONGO_URI, CRAWLER_COLLECTION, DB_NAME, PARSE_COLLECTION, BASE_API_URL


class Parser:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        self.crawler_collection = self.db[CRAWLER_COLLECTION]
        self.parser_collection = self.db[PARSE_COLLECTION]

    def start(self):
        links = self.crawler_collection.find()
        for link in links:
            link = link.get("url")
            product_code = link.split("/")[-1]
            params = {
                "operationName": "ProductDetails",
                "variables": f'{{"productCode":"{product_code}","lang":"en"}}',
                "extensions": '{"persistedQuery":{"version":1,"sha256Hash":"18006c9fd3796b52136051c77d1c05b451b18ce72e6fdb191570da1de6d2089e"}}'
            }
            response = requests.get(BASE_API_URL, params=params)
            if response.status_code == 200:
                self.parse_item(link,response)
            else:
                logging.error(response.status_code)

    def parse_item(self, url, response):
        product = response.json().get("data", {}).get("productDetails",{})
        price_details = product.get("price",{})
        images = product.get("images", [])

        name = product.get("name","")
        product_code =  product.get("code","")
        currency = price_details.get("currencySymbol","")
        price = price_details.get("unitPrice","")
        price_per_unit =  price_details.get("supplementaryPriceLabel1","")

        ingredients = ""
        if product.get("wsNutriFactData"):
            ingredients = product["wsNutriFactData"].get("ingredients", "")

        nutri_score_letter = product.get("nutriScoreLetter","")
        description = product.get("description","")

        images_url = [
           "https://www.delhaize.be" + img["url"] 
           for img in images
           if img.get("format") == "product"
        ]

        item = {
            "product_url":url,
            "name":name,
            "product_code":product_code,
            "currency":currency,
            "price":price,
            "price_per_unit":price_per_unit,
            "ingredients":ingredients,
            "nutri_score_letter":nutri_score_letter,
            "description":description,
            "imges_url":images_url
        }
        logging.info(item)
        self.parser_collection.insert_one(item)



parser = Parser()
parser.start()