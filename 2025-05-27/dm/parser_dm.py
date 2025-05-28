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

        product_name = data["title"]["headline"]
        product_code = data.get("gtin")
        currency = data.get("metadata",{}).get("currency","")
        price = data.get("metadata",{}).get("price",0)
        brand = data.get("brand", {}).get("name", "")
        images = data.get("images", [{}])
        breadcrumb = data.get("breadcrumbs", [])
        rating = data.get("rating", {}).get("ratingValue", 0)
        review = data.get("rating").get("ratingCount",0)

        images = [image["src"] for image in images]
        features = ""
        description = ""
        ingredients = ""
        storage_instructions = ""
        warning = ""
        company_address = ""
        nutritional_information = ""
        manufacturer_address = ""
        

        for group in data.get("descriptionGroups",[]):
            header = group.get("header")
            content_block = group.get("contentBlock", [])

            if header == "Značilnosti":
                features = content_block[0]["descriptionList"][0]["description"]

            if header == "Opis izdelka":
                for block in content_block:
                    if "texts" in block:
                        description = block["texts"][0]
                        break
            
            if header == "Sestavine" and "texts" in content_block[0]:
                raw_ingredients = content_block[0]["texts"][0]
                ingredients = raw_ingredients.replace("\n", " ") 
            
            if header == "Navodila za shranjevanje":
                storage_instructions = content_block[0]["texts"][0]

            if header == "Opozorila":
                warning = content_block[0]["texts"][0]

            if header == "Naslov podjetja":
                raw_company_address = content_block[0]["texts"][0]
                company_address = raw_company_address.replace("\n"," ")
            
            if header == "Hranilne vrednosti":
                table = content_block[0].get("table", [])
                nutritional_information = {
                    raw[0]:raw[1] for raw in table[1:]
                }
            
            if header == "Proizvedeno v":
                manufacturer_address = content_block[0]["texts"][0]

        if breadcrumb:
            breadcrumb = " > ".join(breadcrumb)

        item = {}

        item["pdp_url"] = link
        item["product_name"] = product_name
        item["product_code"] = product_code
        item["product_price"] = price   
        item["currency"] = currency
        item["brand"] = brand   
        item["images"] = images
        item["breadcrumb"] = breadcrumb
        item["rating"] = rating
        item["review"] = review
        item["features"] = features
        item["product_description"] = description
        item["ingredients"] = ingredients
        item["storage_instructions"] = storage_instructions
        item["warning"] = warning 
        item["company_address"] = company_address
        item["nutritional_information"] = nutritional_information
        item["manufacturer_address"] = manufacturer_address

        logging.info(item)
        self.parser_collection.insert_one(item)



parser = Parser()
parser.start()