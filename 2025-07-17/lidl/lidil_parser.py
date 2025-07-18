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

            if self.parser_collection.find_one({"pdp_url": link}):
                logging.info(f"Skipping already parsed URL: {link}")
                continue

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
        CARE_INSTRUCTIONS = "//p[strong[contains(text(), 'Onderhoudsinstructies')]]/following-sibling::*[1]//text()"
        BRAND_XPATH = '//a[@class="heading__brand"]/text()'
        PROPERTIES_XPATH = "//p[strong[contains(text(), 'Eigenschappen')]]/following-sibling::ul/li/text()"
        SIZE_XPATH =     '//fieldset[.//span[@class="attribute-label__name" and text()="maten:"]]//ul[contains(@class,"attributes-one__options")]//label/text()'
        SCRIPT_DATA_XPATH = '//script[@id="__NUXT_DATA__"]/text()'
        COLOR_XPATH = '//p[strong[contains(text(), "Kleuren") or contains(text(), "Kleur")]]/text()[1]'


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
        care_instructions = sel.xpath(CARE_INSTRUCTIONS).getall()
        properties = sel.xpath(PROPERTIES_XPATH).getall()
    
        features = {}
        for row in sel.xpath('//table//tr'):
            key = row.xpath('./td[1]//strong/text()').get()
            value = row.xpath('./td[2]//text()').get()
            if key and value:
                features[key.strip().rstrip(':')] = value.strip()
                
        price_was = f"{float(price_was.strip().replace('-', '')):.2f}" if price_was and price_was.strip() else "0.00"
        percentage_discount = percentage_discount.replace('-','').strip() if percentage_discount else ""
        selling_price = f"{float(selling_price.replace('-','')):.2f}" 
        review = review.replace("(","").replace(")","") if review else ""
        rating = rating.replace("/5","") if rating else ""
        breadcrumb = " > ".join(breadcrumb) if breadcrumb else ""
        brand = brand.strip() if brand else ""

        if size:
            size = [s.strip() for s in size]
            size = list(set(size))
        else:
            size = []

        color = color.replace(";",",") if color else "" 
        care_instructions = ", ".join(care_instructions) if care_instructions else ""
        properties = ", ".join(properties) if properties else ""


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
        item["care_instructions"] = care_instructions
        item["properties"] = properties
        item["features"] = features

        logging.info(item)

        try:
            ProductItem(**item).save()
        except:
            pass

if __name__ == "__main__":
    parser = Parser()
    parser.start()


