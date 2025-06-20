import requests
import logging
from settings import HEADERS, MONGO_URI, CRAWLER_COLLECTION, DB_NAME
from pymongo import MongoClient
from parsel import Selector
import re


class Crawler:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        self.collection = self.db[CRAWLER_COLLECTION]
    
    def start(self):
        url = "https://mmlafleur.com/collections/dresses"
        response = requests.get(url,headers=HEADERS)

        if response.status_code:
            sel = Selector(response.text)
            script_text = sel.xpath(
                "//script[@id='web-pixels-manager-setup']/text()").get()
            
            product_urls = re.findall(r'"url":"(/products/[^"]+)"', script_text)
            for url in product_urls:
                pdp_url = {"url":f"https://mmlafleur.com{url}"}
                logging.info(pdp_url)
                self.collection.insert_one(pdp_url)
        else:
            logging.error(response.status_code)


if __name__ == "__main__":
    crawler = Crawler()
    crawler.start()