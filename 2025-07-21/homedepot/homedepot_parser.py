import requests
from mongoengine import connect
import json
import logging
from parsel import Selector
from pymongo import MongoClient
from homedepot_items import  FailedItem, ProductItem
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
        logging.info(link)
        sel = Selector(response.text)


        breadcrumb = sel.xpath('//div[contains(@class,"breadcrumb__item")]/a/text()').getall()
        retail_limit = sel.xpath('//div[contains(text(), "per order")]/text()').get()
        json_ld_text = sel.xpath("//script[@id='thd-helmet__script--productStructureData']/text()").get()
        details_script = sel.xpath('//script[contains(text(), "window.__APOLLO_STATE__")]/text()').get()

        product_data = json.loads(json_ld_text)

        product_name = product_data.get("name")
        brand = product_data.get("brand", {}).get("name")
        images = product_data.get("image", [])
        offers = product_data.get("offers", {})


        aggregate_rating = product_data.get("aggregateRating", {})
        rating = aggregate_rating.get("ratingValue", "")
        review = aggregate_rating.get("reviewCount", "")

        product_description = product_data.get("description", "")
        currency = offers.get("priceCurrency", "")
        price_was = offers.get("priceSpecification", {}).get("price", "")
        selling_price = offers.get("price", "")

        # product details
        start = details_script.find('{')
        end = details_script.rfind('}') + 1
        apollo_data = json.loads(details_script[start:end])

        for key in apollo_data:
            if key.startswith("base-catalog-"):
                base_data = apollo_data[key]
                break

        product_details = {}
        groups = base_data.get("specificationGroup", [])
        for group in groups:
            for spec in group.get("specifications", []):
                product_details[spec["specName"]] = spec["specValue"]

        
        breadcrumb = " > ".join(breadcrumb) 
        retail_limit = retail_limit.strip() if retail_limit else ""
        brand = brand.strip() if brand else ""
        rating = rating.strip() if rating else ""
        review = str(review).strip() if review else ""
        product_description = product_description.strip() if product_description else ""
        currency = currency.strip() if currency else ""
        price_was = str(price_was).strip() if price_was else "0.00"

        
        item = {}

        item["pdp_url"] = link
        item["product_name"] = product_name
        item["brand"] = brand
        item["breadcrumb"] = breadcrumb
        item["retail_limit"] = retail_limit
        item["currency"] = currency
        item["selling_price"] = selling_price
        item["price_was"] = price_was
        item["images"] = images
        item["rating"] = rating
        item["review"] = review
        item["product_description"] = product_description
        item["product_details"] = product_details

        logging.info(item)

        try:
            ProductItem(**item).save()
        except:
            pass


if __name__ == "__main__":
    parser = Parser()
    parser.start()
