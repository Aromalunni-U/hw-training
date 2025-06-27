import requests
from mongoengine import connect
import logging
from parsel import Selector
from pymongo import MongoClient
from almayaonline_items import ProductItem, FailedItem
from settings import MONGO_URI, DB_NAME,HEADERS, CRAWLER_COLLECTION


class Parser:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
        self.client = MongoClient(MONGO_URI)
        self.crawler_collection = self.client[DB_NAME][CRAWLER_COLLECTION]

    def start(self):
        links = self.crawler_collection.find()

        for link in links:
            link = link.get("url","")

            response = requests.get(link,headers=HEADERS)
            if response.status_code == 200:
                self.parse_iem(link,response)
            else:
                product_item = FailedItem(url = link, source ="parser")
                product_item.save()
                
    def parse_iem(self,url,response):
        sel = Selector(response.text)

        page_title = sel.xpath("//title/text()").get()
        if page_title and "Almaya. Home page title" in page_title:
            failed_item = FailedItem(url=url, source="parser (homepage)")
            failed_item.save()
            return

        PRODUCT_NAME_XPATH = '//div[contains(@class,"product-name")]/h1/text()'
        UNIQUE_ID_XPATH = '//div[@data-productid]/@data-productid'
        PRICE_XPATH = '//div[@class="product-price"]/span/text()'
        IMAGES_XPATH = '//div[@class="picture"]/img/@src'
        DESCRIPTION_XPATH = '//div[@class="full-description"]//text()'

        product_name = sel.xpath(PRODUCT_NAME_XPATH).get()
        unique_id = sel.xpath(UNIQUE_ID_XPATH).get()
        price = sel.xpath(PRICE_XPATH).get()
        images = sel.xpath(IMAGES_XPATH).get()
        product_description = sel.xpath(DESCRIPTION_XPATH).get()

        if price:
            currency = price.split()[0]
            regular_price = price.split()[1]
        else:
            currency, regular_price = "", ""

        product_description = product_description.strip() if product_description else ""
        
        item = {}

        item["pdp_url"] = url
        item["product_name"] = product_name
        item["unique_id"] = unique_id
        item["currency"] = currency
        item["regular_price"] = regular_price
        item["images"] = images
        item["product_description"] = product_description

        logging.info(item)
        product_item = ProductItem(**item)
        product_item.save()


if __name__ == "__main__":
    parser_obj = Parser()
    parser_obj.start()
