import re
import requests
import logging
from pymongo import MongoClient
from settings import MONGO_URI, CRAWLER_COLLECTION, PARSE_COLLECTION, DB_NAME, BASE_URL_PRODUCT, USER_AGENTS, HEADERS
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
            product_code = re.search(r'p(\d+)\.html', link).group(1)
            url = BASE_URL_PRODUCT.format(product_code)
            HEADERS["user-agnet"] = random.choice(USER_AGENTS)
            
            response = requests.get(url,headers=HEADERS)
            if response.status_code == 200:
                self.parse_item(link, response)
                
                
    def parse_item(self,link, response):
        data = response.json()

        product_code = data.get("gtin")
        currency = data.get("metadata",{}).get("currency","")
        price = data.get("metadata",{}).get("price",0)
        brand = data.get("brand", {}).get("name", "")
        images = data.get("images", [{}])[0].get("src")
        breadcrumb = data.get("breadcrumbs", [])
        rating = data.get("rating", {}).get("ratingValue", 0)
        review = data.get("rating").get("ratingCount",0)

        description = ""
        warning = ""

        for group in data.get("descriptionGroups",[]):
            header = group.get("header")

            if header == "Opis izdelka":
                for block in group.get("contentBlock", []):
                    if "texts" in block:
                        description = block["texts"][0]
                        break
            
            if header == "Opozorila":
                content_block = group.get("contentBlock", [])
                if content_block and "texts" in content_block[0]:
                    warning = content_block[0]["texts"][0]


        if breadcrumb:
            breadcrumb = " > ".join(breadcrumb)

        item = {}

        item["pdp_url"] = link
        item["product_code"] = product_code
        item["product_price"] = price   
        item["currency"] = currency
        item["brand"] = brand   
        item["images"] = images
        item["breadcrumb"] = breadcrumb
        item["rating"] = rating
        item["review"] = review
        item["product_description"] = description
        item["warning"] = warning 

        logging.info(item)
        self.parser_collection.insert_one(item)



parser = Parser()
parser.start()