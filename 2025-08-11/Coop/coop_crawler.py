import requests
import logging
import json
from coop_items import  FailedItem, ProductUrlItem
from mongoengine import connect
from pymongo import MongoClient
from parsel import Selector
from settings import (
    MONGO_URI, DB_NAME,
    MONGO_COLLECTION_CATEGORY, headers
)   


class Crawler:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
        self.client = MongoClient(MONGO_URI)
        self.category_collection = self.client[DB_NAME][MONGO_COLLECTION_CATEGORY]
    
    def start(self):
        for category_url in self.category_collection.find():
            url = category_url.get("url","")

            session = requests.Session()

            cookies = {
            'datadome': '1~YZyQTI1fW9TJncY9NnIqrboYiuFA4R5wkf2AhJpBj38wDin6UyxI7EZyUUk3Qfu4jRDDJC4G48KGoM4BE9Mqr_O1tSGREzEwP7VfpsKCoGJusDdt2b6MIK5m0TNJZ7'
            }
            logging.info(url)
            while True:
                response = session.get(url=url,headers=headers, cookies=cookies)
                if response.status_code == 200:
                    sel = Selector(response.text)

                    data = sel.xpath("//script[@type='application/ld+json' and contains(text(), '\"ItemList\"')]/text()").get()
                    try:
                        json_data = json.loads(data)
                        product_list = json_data.get("itemListElement", [])
                        urls = [product.get("url") for product in product_list if product.get("url")]

                        pdp_urls = [url.replace(":443", "") for url in urls]

                        for url in pdp_urls:
                            logging.info(url)


                        next_page = sel.xpath('//a[@class="pagination__next"]/@href').get()
                        if not next_page:
                            break
                        url = f"https://www.coop.ch{next_page}"
                    except Exception as e:
                        logging.error(f"Error : {e}")
                        break

                else:
                    logging.error(f"Status code :{response.status_code}")



if __name__ == "__main__":
    crawler = Crawler()
    crawler.start()