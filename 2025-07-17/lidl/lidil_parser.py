import json
import requests
from mongoengine import connect
import logging
from parsel import Selector
from pymongo import MongoClient
from lidil_items import  FailedItem, ProductItem
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
    
    def parse_item(self,link, response):
        sel = Selector(response.text)

        PRODUCT_NAME_XPATH = '//h1[@class="heading__title"]/text()'
        PRICE_WAS_XPATH = '//div[@class="ods-price__stroke-price"]/s/text()'
        PERCENTAGE_DESCOUNT_XPATH = '//span[@class="ods-price__box-content-text-el"]/text()'
        SELLING_PRICE_XPATH = '//div[@class="ods-price__value"]/text()'
        IMAGES_XPATH = '//img[@class="thumbnail-slide__image"]/@src'
        REVIEW_XPATH = '//span[@class="ods-rating__info-total"]/text()'
        RATING_XPATH = '//span[@class="ods-rating__info"]/text()'
        BREADCRUMB_XPATH = '//span[@class="ods-breadcrumbs__link-title"]/text()'
        MATERIAL_XPATH = "//p[strong[contains(text(), 'Materiaal')]]/following-sibling::*[1]//text()"
        CARE_INSTRUCTIONS = "//p[strong[contains(text(), 'Onderhoudsinstructies')]]/following-sibling::*[1]//text()"
        BRAND_XPATH = '//a[@class="heading__brand"]/text()'
        PROPERTIES_XPATH = "//p[strong[contains(text(), 'Eigenschappen')]]/following-sibling::ul/li/text()"
        SIZE_XPATH = '//ul[@class="attributes-one__options"]//label[@class="option"]/text()'
        SCRIPT_DATA_XPATH = '//script[@id="__NUXT_DATA__"]/text()'
        COLOR_XPATH = '//p[strong[contains(text(), "Kleuren")]]/text()[1]'


        product_name = sel.xpath(PRODUCT_NAME_XPATH).get()
        price_was = sel.xpath(PRICE_WAS_XPATH).get()
        percentage_discount = sel.xpath(PERCENTAGE_DESCOUNT_XPATH).get()
        selling_price = sel.xpath(SELLING_PRICE_XPATH).get()
        images = sel.xpath(IMAGES_XPATH).getall()
        review = sel.xpath(REVIEW_XPATH).get()
        rating = sel.xpath(RATING_XPATH).get()
        breadcrumb = sel.xpath(BREADCRUMB_XPATH).getall()
        brand = sel.xpath(BRAND_XPATH).get()
        size = sel.xpath(SIZE_XPATH).getall()
        script_data = sel.xpath(SCRIPT_DATA_XPATH).get()


        data = json.loads(script_data)
        flat = json.dumps(data)
        decoded_data = flat.encode().decode('unicode_escape')  

        sel = Selector(text=decoded_data)

        color = sel.xpath(COLOR_XPATH).get()
        material = sel.xpath(MATERIAL_XPATH).getall()
        care_instructions = sel.xpath(CARE_INSTRUCTIONS).getall()
        properties = sel.xpath(PROPERTIES_XPATH).getall()

        features = {}
        for row in sel.xpath('//table//tr'):
            key = row.xpath('./td[1]//strong/text()').get()
            value = row.xpath('./td[2]//text()').get()
            if key and value:
                features[key.strip().rstrip(':')] = value.strip()

        percentage_discount = percentage_discount.replace("-","").strip() if percentage_discount else ""
        breadcrumb = " > ".join(breadcrumb) if breadcrumb else ""
        brand = brand.strip() if brand else ""


        item = {}

        item["pdp_url"] = link
        item["product_name"] = product_name
        item["price_was"] = price_was
        item["percentage_discount"] = percentage_discount
        item["selling_price"] = selling_price
        item["images"] = images
        item["review"] = review
        item["rating"] = rating
        item["breadcrumb"] = breadcrumb
        item["brand"] = brand
        item["size"] = size
        item["color"] = color
        item["material"] = material
        item["care_instructions"] = care_instructions
        item["properties"] = properties

        logging.info(item)

      

if __name__ == "__main__":
    parser = Parser()
    parser.start()


