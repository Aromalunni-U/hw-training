import requests
import logging
from pymongo import MongoClient
from settings import MONGO_URI, CRAWLER_COLLECTION, PARSE_COLLECTION, DB_NAME, API_HEADERS, API_URL, USER_AGENTS
from time import sleep
import random

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
            API_HEADERS["referer"] = link
            API_HEADERS["user-agent"] = random.choice(USER_AGENTS)

            payload = {
                "viewName": "MainFlow.ProductDetailsPage",
                "versionInfo": {
                    "moduleVersion": "PuN3d6LB4faGdgG7sxfsDQ",
                    "apiVersion": "11PE+Ajsou80jI7PsgrPjg"
                },
                "screenData": {
                    "variables": {
                        "SKU": link.split("-")[-1]
                    }
                }
                }
            
            response = requests.post(url=API_URL,json=payload, headers=API_HEADERS)
            sleep(0.5)
            if response.status_code == 200:
                self.parse_item(link,response)
            else:
                logging.error(response.status_code)

    def parse_item(self, url, response):
        data = response.json()
        product = data.get("data",{}).get("ProductOut",{})

        product_name = product.get("Overview",{}).get("Name")
        product_price = product.get("Overview",{}).get("Price")
        product_image = product.get("Overview",{}).get("Image",{}).get("URL")
        product_ingredients = product.get("Ingredients")
        nutrients_list = product.get("Nutrient",{}).get("Nutrients").get("List",[])
        base_unit_price = product.get("Overview",{}).get("BaseUnitPrice")
        raw_breadcrumbs = product.get("Categories",{}).get("List")

        nutrients = [
            {
                item.get("Description"): item.get("QuantityContained", {}).get("Value"),
            }
            for item in nutrients_list
        ]

        breadcrumb = " > ".join([data["Name"] for data in raw_breadcrumbs])

        item = {}

        item["product_url"] = url
        item["product_name"] = product_name
        item["product_price"] = product_price
        item["product_image"] = product_image
        item["product_ingredients"] = product_ingredients
        item["product_nutrients"] = nutrients
        item["product_base_unit_price"] = base_unit_price
        item["breadcrumb"] = breadcrumb

        logging.info(item)
        self.parser_collection.insert_one(item)



parser = Parser()
parser.start()