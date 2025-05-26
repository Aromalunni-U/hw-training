import requests
import logging
from settings import HEADERS_CAT_2, BASE_URL, CRAWLER_COLLECTION, MONGO_URI, DB_NAME
from pymongo import MongoClient


class Crawler:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        self.collection = self.db[CRAWLER_COLLECTION]

    def start(self):
        page_no = 1
        while True:
            payload = {
                "versionInfo": {
                    "moduleVersion": "PuN3d6LB4faGdgG7sxfsDQ",
                    "apiVersion": "bYh0SIb+kuEKWPesnQKP1A"
                },
                "viewName": "MainFlow.ProductListPage",
                "screenData": {
                    "variables": {
                        "CategorySlug": "melk-karnemelk",
                        "PageNumber": page_no
                    }
                }
            }

            response = requests.post(BASE_URL, json=payload, headers=HEADERS_CAT_2)

            if response.status_code == 200:

                data = response.json()
                items = data.get("data", {}).get("ProductList", {}).get("List", [])

                if items:
                    for item in items:
                        slug = item.get("PLP_Str", {}).get("Slug")
                        if slug:
                            full_url  = {
                            "url" : "https://www.plus.nl/product/" + slug
                            }
                            logging.info(full_url)
                            # self.collection.insert_one(full_url)
                else:
                    logging.info("Completed successfully")
                    break
                   
                page_no += 1
            else:
                logging.info(response.status_code)
                break


crawler = Crawler()
crawler.start()