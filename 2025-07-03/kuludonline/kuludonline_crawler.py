import requests
import logging
from settings import HEADERS, MONGO_URI, DB_NAME, BASE_URL, MONGO_COLLECTION_CATEGORY
from parsel import Selector
from kuludonline_items import ProductUrlItem, FailedItem
from mongoengine import connect
from pymongo import MongoClient
from urllib.parse import urljoin
from time import sleep


class Crawler:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
        self.client = MongoClient(MONGO_URI)
        self.category_collection = self.client[DB_NAME][MONGO_COLLECTION_CATEGORY]
    
    def start(self):
        for category_url in self.category_collection.find():
            category_url = category_url.get("url","")
            while True:
                response = requests.get(url=category_url, headers=HEADERS)
                if response.status_code == 200:
                    product_found = self.parse_item(response)
                    if not product_found:
                        break

                    sel = Selector(response.text)
                    next_page = sel.xpath('//li[@class="next"]/a/@href').get()
                    if not next_page:
                        break
                    category_url = urljoin(BASE_URL, next_page)
                    sleep(0.5)
                else:
                    logging.warning(f"Status code: {response.status_code}")
                    FailedItem(url=next_page, source="crawler").save()
                    break

    def parse_item(self,response):
        sel = Selector(response.text)

        CARD_XPATH = '//div[contains(@class, "product-item card")]'
        PRODUCT_NAME = './/a[@class="product-item__title"]/@title'
        PRODUCT_URL = './/a[@class="product-item__title"]/@href'
        REGULAR_PRICE = './/span[@class="price "]/text()'
        IMAGE_XPATH = './/img[contains(@class,"img")]/@src'

        cards = sel.xpath(CARD_XPATH)

        if not cards:
            return False

        for card in cards:
            pdp_url = card.xpath(PRODUCT_URL).get()
            product_name = card.xpath(PRODUCT_NAME).get()
            regular_price = card.xpath(REGULAR_PRICE).get()
            image = card.xpath(IMAGE_XPATH).get()

            pdp_url = f"{BASE_URL}{pdp_url}"
            image = f"https:{image}" if image else ""
            regular_price = regular_price.strip() if regular_price else ""

            item = {}

            item["url"] = pdp_url
            item["product_name"] = product_name
            item["regular_price"] = regular_price
            item["image"] = image

            logging.info(item)
            data_item = ProductUrlItem(**item)
            data_item.save()

        return True
    



if __name__ == "__main__":
    crawler = Crawler()
    crawler.start()