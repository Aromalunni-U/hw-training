from curl_cffi import requests
import logging
from netto_items import  FailedItem, ProductUrlItem
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
            logging.info(f"{'#' * 20} {link} {'#' * 20}")

            page_no = 1

            while True:

                url = link if page_no == 1 else f"{link}/{page_no}"

                response = requests.get(url=url, headers=HEADERS , impersonate="chrome")
                if response.status_code == 200:
                    sel = Selector(response.text)

                    pdp_urls = sel.xpath('//div[@class="product clearfix"]/a/@href').getall()

                    if not pdp_urls:
                        break

                    for url in pdp_urls:
                        logging.info(url)
                        try:
                            ProductUrlItem(url = url).save()
                        except:
                            pass
                    
                    page_no +=1

                else:
                    logging.error(f"Status code : {response.status_code}")
                    FailedItem(url = link, source = "crawler").save()
                    break




if __name__ == "__main__":
    crawler = Crawler()
    crawler.start()
