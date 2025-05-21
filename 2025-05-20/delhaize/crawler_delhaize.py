import json
import requests
import logging
from settings import  CRAWLER_COLLECTION, MONGO_URI, DB_NAME
from urllib.parse import urljoin, quote
from pymongo import MongoClient



class Crawler:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        self.collection = self.db[CRAWLER_COLLECTION]

    def start(self):
        page_no = 1
        product_links =[]

        while True:
            variables = {
            "lang": "en",
            "searchQuery": ":relevance",
            "sort": "relevance",
            "category": "v2FRU",
            "pageNumber": page_no,
            "pageSize": 50,
            "filterFlag": True,
            "fields": "PRODUCT_TILE",
            "plainChildCategories": True
            }

            extensions = {
                    "persistedQuery": {
                        "version": 1,
                        "sha256Hash": "4a9b385fdead25bb28350f1968ff36b8c44cf2def250653c8c81cbd3ece02e18"
                    }
                }
            variables_encoded = quote(json.dumps(variables))
            extensions_encoded = quote(json.dumps(extensions))

            API_URL = f"https://www.delhaize.be/api/v1/?operationName=GetCategoryProductSearch&variables={variables_encoded}&extensions={extensions_encoded}"


            response = requests.get(API_URL)

            if response.status_code == 200:
                products = response.json().get("data", {}).get("categoryProductSearch", {}).get("products", [])
                if not products:
                    break

                new_links = []
                for product in products:
                    if "url" in product:
                        product_url = urljoin("https://www.delhaize.be", product["url"])
                        if product_url not in product_links:
                            new_links.append({"url": product_url})

                logging.info(new_links)
                if new_links:
                    self.collection.insert_many(new_links)
                page_no += 1
                
            else:
                logging.error(response.status_code)
                break


crawler = Crawler()
crawler.start()