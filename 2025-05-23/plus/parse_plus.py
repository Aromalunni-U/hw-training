import requests
import logging
from pymongo import MongoClient
from settings import MONGO_URI, CRAWLER_COLLECTION, PARSE_COLLECTION, DB_NAME, BASE_API_URL, PARSER_HEADER
from parsel import Selector

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
            url = BASE_API_URL.format(link)
            
            response = requests.get(url=url, headers=PARSER_HEADER)
            if response.status_code == 200:
                self.parse_item(link,response)
                break
            else:
                logging.error(response.status_code)

    def parse_item(self, url, response):
     pass




parser = Parser()
parser.start()