import requests
import logging
import json
from westside_items import  FailedItem, ProductUrlItem
from mongoengine import connect
from pymongo import MongoClient
from parsel import Selector
from settings import (
    HEADERS, MONGO_URI, DB_NAME,
    MONGO_COLLECTION_CATEGORY, headers, filter_url
)   


class Crawler:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
        self.client = MongoClient(MONGO_URI)
        self.category_collection = self.client[DB_NAME][MONGO_COLLECTION_CATEGORY]
    
    def start(self):
        for category_url in self.category_collection.find():
            category_url = category_url.get("url","")

            response = requests.get(category_url, headers=HEADERS)
            sel = Selector(response.text)

            if response.status_code == 200:
                script = sel.xpath('//script[contains(text(), "Category ID")]/text()').get()
                script_data = script.strip()

                category_id = self.get_category_id(script_data)
                category_name =  category_url.split("/")[-1]

                logging.info(f"{"#" * 20} {category_name} {"#" * 20}")

                page_number = 1
    
                while True:

                    payload = self.get_payload(category_id, category_name , page_number)
                    response = requests.post(filter_url, headers = headers, json = payload)
                    product_found = self.parse_item(response)   

                    if not product_found:
                        break
                    
                    page_number += 1

            else:
                logging.info(f"Status code : {response.status_code}")
                FailedItem(category_url,source = "crawler").save()

    
    def get_category_id(self, raw_data):

        length = len('"Collection View",')
        start = raw_data.find('"Collection View",')
        end = raw_data.find(");")
        data = raw_data[(start + length) : end]

        data = json.loads(data)
        category_id = data.get("Category ID", "")

        return category_id
    
    
    def get_payload(self, category_id, category_name, page_number):
    
        filters = {
            "productsCount": 50,
            "categories": [category_id],  
            "type": "CATEGORY_PAGE",
            "facets": [],
            "getAllVariants": "false",
            "swatch": [{"key": "product_Multi_Variant_Product"}],
            "currency": "INR",
            "sort": [
                {"field": "relevance", "order": "asc"},
                {"field": f"product_{category_name}_sortOrder:float", "order": "asc"}
            ],
            "showOOSProductsInOrder": "true",
            "inStock": [],
            "page": page_number
        }

        payload = {
            "fW": "yes",
            "filters": json.dumps(filters),
            "group": "categoryPage"
        }

        return payload
    
    def parse_item(self, response):
        if response.status_code == 200:
            data = response.json()
            results = data.get("payload", {}).get("result", [])

            if not results:
                return False

            for product in results:
                url = product.get("url", "")
                name = product.get("name", "")
                brand = product.get("brand", "")
                selling_price = product.get("sellingPrice", "")

                item = {}

                item["url"] = url
                item["product_name"] = name
                item["brand"] = brand
                item["selling_price"] = selling_price

                logging.info(item)   
                try:
                    ProductUrlItem(**item).save()
                except:
                    pass

            return True



if __name__ == "__main__":
    crawler = Crawler()
    crawler.start()