import requests
from mongoengine import connect
import logging
from parsel import Selector
from pymongo import MongoClient
from homecentre_items import ProductItem
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
                logging.error(f"Status code : {response.status_code}")

    def parse_item(self,link, response):
        
        sel = Selector(response.text)

        PRODUCT_NAME_XPATH = '//h1[@id="product-details-name"]/text()'
        BREADCRUMB_XPATH = '//ol[@id="breadcrumb"]/li/a/text()'
        PRICE_XPATH = '//span[@itemprop="price"]/@content'
        PRICE_WAS_XPATH = '//del[@id="products-details-price-old-01"]/text()'
        STOCK_XPATH = '//strong[@id="product-stock"]/text()'
        DETAILS_XPATH =  '//div[@id="product-overview-v2"]/p//text()'
        COLOR_XPATH = '//li[@id="colorItem0" or @id="filter-form-colo-item-0"]/input/@data-product-color'
        IMAGE_XPATH = '//span[@data-alt="image description"]/picture//img/@src'
        MATERIAL_XPATH = '//div[@class="attribute-group-v2"][.//p[contains(text(), "Material")]]//div[@class="row"]'
        SPEC_XPATH = '//div[@class="attribute-group-v2"][.//p[contains(text(), "Specifications")]]//div[@class="row"]'

        product_name = sel.xpath(PRODUCT_NAME_XPATH).get()
        breadcrumb = sel.xpath(BREADCRUMB_XPATH).getall()
        price = sel.xpath(PRICE_XPATH).get()
        price_was = sel.xpath(PRICE_WAS_XPATH).get()
        stock = sel.xpath(STOCK_XPATH).get()
        details = sel.xpath(DETAILS_XPATH).getall()
        product_color = sel.xpath(COLOR_XPATH).get()
        image = sel.xpath(IMAGE_XPATH).get()


        material = {}
        specification = {}

        material_data = sel.xpath(MATERIAL_XPATH)
        specification_data = sel.xpath(SPEC_XPATH)

        for data in material_data:
            key = data.xpath('.//div[contains(@class,"attribute-table-key")]/text()').get()
            value = data.xpath('.//div[contains(@class,"attribute-table-value")]/text()').get()
            if key and value:
                material[key.strip()] = value.strip()

        for data in specification_data:
            key = data.xpath('.//div[contains(@class,"attribute-table-key")]/text()').get()
            value = data.xpath('.//div[contains(@class,"attribute-table-value")]/text()').get()
            if key and value:
                specification[key.strip()] = value.strip()

        product_id = link.split("/")[-1]
        breadcrumb = " > ".join(breadcrumb) if breadcrumb else ""
        price_was = price_was.replace(",", "").replace("AED", "").strip() if price_was else ""
        stock = True if stock and "in stock" in stock.strip().lower() else False
        details = " ".join([detail.strip() for detail in details]) if details else ""
        product_color = product_color.strip() if product_color else ""

        item = {}

        item["pdp_url"] = link
        item["product_id"] = product_id
        item["product_name"] = product_name
        item["product_color"] = product_color
        item["material"] = material
        item["details"] = details
        item["specification"] = specification
        item["price"] = price
        item["price_was"] = price_was
        item["breadcrumb"] = breadcrumb
        item["stock"] = stock
        item["image"] = image

        logging.info(item)
        try:
            ProductItem(**item).save()
        except:
            pass

if __name__ == "__main__":
    parser = Parser()
    parser.start()
