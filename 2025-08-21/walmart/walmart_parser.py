import json
import requests
from mongoengine import connect
import logging
from parsel import Selector
from pymongo import MongoClient
from walmart_items import ProductItem, FailedItem
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
                logging.error(f"Status code : {response.status_code}")
                FailedItem(
                        url = link,
                        source = "parser",
                        status_code = response.status_code
                    ).save()
    
    
    def parse_item(self,link, response):
        sel = Selector(response.text)

        PRODUCT_NAME_XPATH = '//h1/text()'
        SELLING_PRICE_XPATH = '//span[@itemprop="price"]/text()'
        REGULAR_PRICE_XPATH = '//span[@data-seo-id="strike-through-price"]/text()'
        IMAGE_XPATH = '//div[@class="relative db"]/img/@src'
        RATING_XPATH = '//span[@class="f7 ph1"]/text()'
        REVIEW_XPATH = '//a[@itemprop="ratingCount"]/text()'
        INGREDIENTS_XPATH = '//h3[contains(text(), "Ingredients")]/following-sibling::p/text()'
        SCRIPT_DATA = '//script[@id="__NEXT_DATA__"]/text()'
        PROMO_DESCRIPTION_XPATH = '//div[@data-testid="dollar-saving"]//text()'


        product_name = sel.xpath(PRODUCT_NAME_XPATH).get()
        selling_price = sel.xpath(SELLING_PRICE_XPATH).get()
        regular_price = sel.xpath(REGULAR_PRICE_XPATH).get()
        image = sel.xpath(IMAGE_XPATH).get()
        rating = sel.xpath(RATING_XPATH).get()
        review = sel.xpath(REVIEW_XPATH).get()
        ingredients = sel.xpath(INGREDIENTS_XPATH).get()
        promo_description = sel.xpath(PROMO_DESCRIPTION_XPATH).get()
        
        json_ld = sel.xpath(SCRIPT_DATA).get()
        try:
            data = json.loads(json_ld)
        except:
            return
      

        product = data.get("props", {}).get("pageProps", {}).get("initialData", {}).get("data", {})
        product_description = product.get("product", {}).get("shortDescription", "")
        warning = product.get("idml", {}).get("warnings", [])
        specs_list = product.get("idml", {}).get("specifications", [])
        
        
        if specs_list:
            specification = {
                spec.get("name", "").strip() : spec.get("value", "").strip()
                for spec in specs_list if spec.get("name")
            }
        else:
            specification = {}
        
        selling_price = selling_price.replace("$", "").strip() if selling_price else 0
        regular_price = regular_price.replace("$", "").strip() if regular_price else 0
        image = image.split("?")[0] if image else ""
        rating = rating.replace("(", "").replace(")", "").strip() if rating else ""
        review = review.replace(",", "").replace("ratings", "").strip() if review else ""
        ingredients = ingredients if ingredients else ""
        warning = warning[0].get("value", "") if warning else ""
        promotion_description = promo_description.strip() if promo_description else ""
        product_description = (
            product_description.replace("\n", "").replace("\t", "").replace("\r", "").strip()
            if product_description else ""
        )
        
        
        item = {}
        
        item["pdp_url"] = link
        item["product_name"] = product_name
        item["selling_price"] = selling_price
        item["regular_price"] = regular_price
        item["image"] = image
        item["rating"] = rating
        item["review"] = review
        item["ingredients"] = ingredients
        item["warning"] = warning
        item["specification"] = specification
        item["promotion_description"] = promotion_description
        item["product_description"] = product_description
        
        
        
        logging.info(item)
        try:
            ProductItem(**item).save()
        except:
            pass
        


if __name__ == "__main__":
    parser = Parser()
    parser.start()
