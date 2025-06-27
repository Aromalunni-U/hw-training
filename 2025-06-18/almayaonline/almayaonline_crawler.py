import requests
import logging
from settings import HEADERS, MONGO_URI, DB_NAME, BASE_URL, MONGO_COLLECTION_CATEGORY
from parsel import Selector
from almayaonline_items import ProductUrlItem, FailedItem
from mongoengine import connect
from pymongo import MongoClient
from urllib.parse import urlparse


class Crawler:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
        self.client = MongoClient(MONGO_URI)
        self.category_collection = self.client[DB_NAME][MONGO_COLLECTION_CATEGORY]
    
    def start(self):
        for category_url in self.category_collection.find():
            category_url = category_url.get("url","")
            logging.info(f"{'#'*30} {category_url} {'#'*30}")
            self.scrape_category_pages(category_url)

    def scrape_category_pages(self, category_url):
        parsed = urlparse(category_url)
        category_path = parsed.path.strip("/") 
        base_category_url = f"{BASE_URL}/{category_path}"

        page_number = 1
        while True:
                if page_number == 1:
                    paged_url = base_category_url
                else:
                    paged_url = f"{base_category_url}?pagenumber={page_number}"     

                response = requests.get(paged_url, headers=HEADERS)

                if response.status_code == 200:
                    sel = Selector(response.text)
                    product_urls = sel.xpath('//h2[@class="product-title"]/a/@href').getall()

                    if not product_urls:
                        logging.info(f"Category Completed : {base_category_url}")
                        break

                    self.parse_item(sel)
                    page_number += 1

                else:
                    logging.error(f"Status code : {response.status_code}")
                    failed_url = FailedItem(url = base_category_url, source="crawler")
                    failed_url.save()
                    break


 
    def parse_item(self, selector):

        PRODUCT_CARD_XPATH = '//div[contains(@class,"product-item")]'
        PRODUCT_URL_XPATH = './/h2[@class="product-title"]/a/@href'
        PRODUCT_NAME_XPATH = './/h2[@class="product-title"]/a/text()'
        PRICE_XPATH = './/span[@class="price actual-price"]/text()'
        IMAGES_XPATH = './/div[@class="picture"]/a/img/@src'

        product_card = selector.xpath(PRODUCT_CARD_XPATH)

        for card in product_card:

            product_url = card.xpath(PRODUCT_URL_XPATH).get()
            product_name = card.xpath(PRODUCT_NAME_XPATH).get()
            price = card.xpath(PRICE_XPATH).get()
            images = card.xpath(IMAGES_XPATH).get()

            pdp_url =  f"https://www.almayaonline.com{product_url}"
            currency = price.split()[0] if price else ""
            selling_price = price.split()[1] if price else ""

            item = {}

            item['url'] = pdp_url
            item['product_name'] = product_name
            item['regular_price'] = selling_price
            item['currency'] = currency
            item['images'] = images
    
            logging.info(item)
            data_item = ProductUrlItem(**item)
            data_item.save()
            

if __name__ == "__main__":
    crawler = Crawler()
    crawler.start()
