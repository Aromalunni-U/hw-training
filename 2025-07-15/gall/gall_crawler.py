import requests
import logging
import re
from gall_items import  FailedItem, ProductUrlItem
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

            while True:

                response = requests.get(link, headers= HEADERS)

                if response.status_code == 200:

                    self.parse_item(response)
                    sel = Selector(response.text)
                    next_page = sel.xpath("//a[@aria-label='volgende pagina']/@href").get()

                    if not next_page:
                        break

                    link = f"https://www.gall.nl{next_page}"

                else:
                    logging.error(f"Status code {response.status_code}")
                    FailedItem(link, source = "crawler")
        
    def parse_item(self, response):
        
        sel = Selector(response.text)

        PDP_URL_XPATH = './/a[@class="ptile_link"]/@href'
        PRODUCT_NAME_XPATH = './/strong[@itemprop="name"]/text()'
        REGULAR_PRICE_XPATH = './/strong[@class="price ptile_price"]/@aria-label'
        ALCHOLE_VOL_XPATH = './/p[@class="ptile_desc"]/i/text()'
        IMAGE_XPATH = './/img/@src'

        product_card = sel.xpath('//div[@class="ptile "]')

        for card in product_card:
            pdp_url = card.xpath(PDP_URL_XPATH).get()
            product_name = card.xpath(PRODUCT_NAME_XPATH).get()
            regular_price = card.xpath(REGULAR_PRICE_XPATH).get()
            alchole_by_volume = card.xpath(ALCHOLE_VOL_XPATH).get()
            image = card.xpath(IMAGE_XPATH).get()

            pdp_url = f"https://www.gall.nl{pdp_url}"
            regular_price = re.search(r"\d+\.\d+", regular_price).group()
            image = image.split("?")[0] if image else ""

            item = {}

            item["url"] = pdp_url
            item["product_name"] = product_name
            item["regular_price"] = regular_price
            item["alchole_by_volume"] = alchole_by_volume
            item["image"] = image

            logging.info(item)
            try:
                ProductUrlItem(**item).save()
            except:
                pass


if __name__ == "__main__":
    crawler = Crawler()
    crawler.start()
