import requests
from parsel import Selector
from settings import search_url, ean_list ,HEADERS, CRAWLER_COLLECTION, MONGO_URI, DB_NAME
import logging
from pymongo import MongoClient



class Crawler:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        self.collection = self.db[CRAWLER_COLLECTION]

    def start(self):
        for ean in ean_list:
            response = requests.get(search_url.format(ean), headers=HEADERS)
            sel = Selector(response.text)
            relative_urls = sel.xpath('//a[@class="product-tile_wrapper__T0IlX"]/@href').getall()

            if relative_urls:
                full_urls = [{"url":"https://www.petsathome.com" + url} for url in relative_urls]
                for url in full_urls:
                    logging.info(url)
                    self.collection.insert_one(url)
            

crawler = Crawler()
crawler.start()