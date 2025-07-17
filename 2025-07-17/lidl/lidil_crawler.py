import re
import requests
import logging
from lidil_items import  FailedItem, ProductUrlItem
from mongoengine import connect
from pymongo import MongoClient
from parsel import Selector
from settings import (
    HEADERS, MONGO_URI, DB_NAME,
    MONGO_COLLECTION_CATEGORY, 
)   


class Crawler:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
        self.client = MongoClient(MONGO_URI)
        self.category_collection = self.client[DB_NAME][MONGO_COLLECTION_CATEGORY]
    
    def start(self):
        for category_url in self.category_collection.find():
            link = category_url.get("url","")
            logging.info(f"{"#" * 20} {link} {"#" * 20}")

            offset = 0
            while True:

                url = f"{link}?offset={offset}"
                response = requests.get(url, headers = HEADERS)

                sel = Selector(response.text)
                data = sel.xpath('//script[@type="application/json"]/text()').get()

                if data:
                    pdp_urls = re.findall(r'\/p\/[a-zA-Z0-9\-/]+', data)
                    pdp_urls = [f"https://www.lidl.nl{url}" for url in pdp_urls]

                    for url in pdp_urls:
                        logging.info(url)

                        try:
                            ProductUrlItem(url=url).save()
                        except:
                            pass

                    if not pdp_urls:
                        break
                else:
                    break

                offset += 48


if __name__ == "__main__":
    crawler = Crawler()
    crawler.start()
