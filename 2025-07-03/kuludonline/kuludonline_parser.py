import requests
from mongoengine import connect
import logging
from parsel import Selector
from pymongo import MongoClient
from kuludonline_items import  FailedItem, ProductItem
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
        
    
    def parse_item(self,link,response):
        sel = Selector(response.text)

        PRODUCT_NAME_XPATH = '//span[@class="product__title"]/text()'
        INSTOCK_XPATH = '//div[contains(@class, "left-quant")]/text()[normalize-space()]'
        DISCOUNT_XPATH = '//span[@class="product-item__badge product-item__badge--sale"]//text()'
        SALE_PRICE_XPATH = '//span[@class="price "]/text()'
        MRP_XPATH = '//del[@class="product-price--compare"]'


        prouct_name = sel.xpath(PRODUCT_NAME_XPATH).get()
        instock = sel.xpath(INSTOCK_XPATH).get()
        discount = sel.xpath(DISCOUNT_XPATH).get()
        sale_price = sel.xpath(SALE_PRICE_XPATH).get()
        mrp = sel.xpath(MRP_XPATH).re_first(r'\d+\.\d+')

        sale_price = sale_price.replace(",","").strip() if sale_price else ""
        discount = discount.strip() if discount else ""
        mrp = mrp.strip() if mrp else ""
        instock = instock.strip().lower() == "in stock" if instock else False

        item = {}

        item["pdp_url"] = link
        item["product_name"] = prouct_name
        item["instock"] = instock
        item["discount"] = discount
        item["sale_price"] = sale_price
        item["mrp"] = mrp

        logging.info(item)
        product_item = ProductItem(**item)
        product_item.save()


if __name__ == "__main__":
    parser = Parser()
    parser.start()
