import requests
import logging
from settings import HEADERS, MONGO_URI, CRAWLER_COLLECTION, DB_NAME, BASE_URL
from pymongo import MongoClient
from parsel import Selector


class Crawler:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        self.collection = self.db[CRAWLER_COLLECTION]
    
    def start(self):
        response = requests.get(BASE_URL,headers=HEADERS)
        sel = Selector(response.text)
        categories = sel.xpath('//li[@class="all-categories"]/ul/li/a/@href').getall()
        category_urls = [BASE_URL + url  for url in categories]

        for url in category_urls:
                self.scrape_category_pages(url)

    def scrape_category_pages(self, category_url):
         while category_url:
                response = requests.get(category_url, headers=HEADERS)

                if response.status_code == 200:
                    sel = Selector(response.text)

                    self.scrape_pdp_links(sel)

                    next_page = sel.xpath('//li[@class="next-page"]/a/@href').get()
                    category_url = next_page if next_page else None
                else:
                     logging.warning(f"Failed ({response.status_code}):{category_url}")

    def scrape_pdp_links(self, selector):
        product_urls = selector.xpath('//h2[@class="product-title"]/a/@href').getall()

        for url in product_urls:
            pdp_url = {"url":f"https://www.almayaonline.com{url}"}
            logging.info(pdp_url)
            self.collection.insert_one(pdp_url)
            
        
crawler = Crawler()
crawler.start()