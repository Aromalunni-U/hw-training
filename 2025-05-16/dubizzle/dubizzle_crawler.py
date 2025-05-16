import logging
from parsel import Selector
from urllib.parse import urljoin
from settings import *
from pymongo import MongoClient
from curl_cffi import requests


class Crawler:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        self.collection = self.db[CRAWLER_COLLECTION]

    def start(self):
            current_url = BASE_URL
            page_no = 1
            while current_url:
                response = requests.get(current_url, impersonate="chrome", timeout=60)
                if response.status_code == 200:
                    current_url = self.parse_item(response)
                    logging.info(f"Page {page_no} completed")
                    page_no += 1
               
    def parse_item(self, response):
        sel = Selector(response.text)

        links_xpath = "//div[@class='_70cdfb32']/a/@href"
        links = sel.xpath(links_xpath).getall()

        links = [urljoin(BASE_URL, l) for l in links]
        data = [{"links": link} for link in links]
        if data:
            self.collection.insert_many(data) 

        pagination_xpath = "//a[div[@title='Next']]/@href"
        pagination = sel.xpath(pagination_xpath).get()

        if pagination:
             return urljoin(BASE_URL, pagination)
        else:
            logging.info("Pagination completed")
            return None
      

crawler = Crawler()
crawler.start()
