import requests
from mongoengine import connect
import logging
from parsel import Selector
from pymongo import MongoClient
from westside_items import  FailedItem, ProductItem
from settings import MONGO_URI, DB_NAME, HEADERS, CRAWLER_COLLECTION, PARSE_COLLECTION



class Parser:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
        self.client = MongoClient(MONGO_URI)
        self.crawler_collection = self.client[DB_NAME][CRAWLER_COLLECTION]
        self.parser_collection = self.client[DB_NAME][PARSE_COLLECTION]

    def start(self):
        links = self.crawler_collection.find()

        for link in links:
            link = link.get("url","")

            response = requests.get(link,headers=HEADERS)
            if response.status_code == 200:
                self.parse_item(link,response)
            else:
                product_item = FailedItem(url = link, source ="parser")
                product_item.save()



if __name__ == "__main__":
    parser = Parser()
    parser.start()
