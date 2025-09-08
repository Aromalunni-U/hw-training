import json
import requests
from mongoengine import connect
import logging
from parsel import Selector
from pymongo import MongoClient
from mrosupply_items import ProductItem, FailedItem
from settings import MONGO_URI, DB_NAME, HEADERS, CRAWLER_COLLECTION, PARSE_COLLECTION
from datetime import datetime



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
                self.parse_item(response, link)
            else:
                logging.warning(f"Status code : {response.status_code}")
                FailedItem(url=link, sourcce = "parser").save()
            
            
    def parse_item(self, response, link):
        sel = Selector(response.text)
        
        
        BRAND_NAME_XPATH = '//a[@class="js-brand-name"]/text()'
        VENDOR_SELLER_PART_NUMBER_XPATH = '//div[p[contains(text(), "SKU")]]/following-sibling::div/p/text()' 
        ITEM_NAME_XPATH = '//h1/text()'
        FULL_PRODUCT_DESCRIPTION_XPATH = '//div[@class="m-accordion--item--body"]//text()'
        PRICE_XPATH = '//p[contains(@class,"price")]/text()'
        UPC_XPATH = '//div[p[contains(text(), "UPC")]]/following-sibling::div/p/text()'        
        MODEL_NUMBER_XPATH = '//p[@class="modelNo"]/text()'
        PRODUCT_CATEGORY_XPATH = '//ul[@class="m-breadcrumbs-list"]/li[last()]//span/text()'
        date_crawled = datetime.now().strftime("%Y-%m-%d")

        brand = sel.xpath(BRAND_NAME_XPATH).get()
        vendor_seller_part_number = sel.xpath(VENDOR_SELLER_PART_NUMBER_XPATH).get()
        item_name = sel.xpath(ITEM_NAME_XPATH).get()
        product_description = sel.xpath(FULL_PRODUCT_DESCRIPTION_XPATH).getall()
        price = sel.xpath(PRICE_XPATH).get()
        upc = sel.xpath(UPC_XPATH).get()
        model_number = sel.xpath(MODEL_NUMBER_XPATH).get()
        product_category = sel.xpath(PRODUCT_CATEGORY_XPATH).get()
        
        
        brand = brand.strip() if brand else ""
        vendor_seller_part_number = (
            vendor_seller_part_number.strip()
            if vendor_seller_part_number else ""
        )
        item_name = item_name.strip() if item_name else ""
        price = price.strip() if price else "0"
        upc = upc.strip() if upc else ""
        model_number = model_number.strip() if model_number else ""
        product_category = product_category.strip() if product_category else ""
        
        
        item = {}
                
        item["pdp_url"] = link
        item["brand"] = brand
        item["vendor_Seller_part_number"] = vendor_seller_part_number
        item["item_name"] = item_name 
        item["product_description"] = product_description
        item["price"] = price
        item["upc"] = upc
        item["model_number"] = model_number
        item["product_category"] = product_category
        item["date_crawled"] = date_crawled
        
        logging.info(item)
        
        try:
            ProductItem(**item).save()
        except:
            pass



if __name__ == "__main__":
    parser = Parser()
    parser.start()
