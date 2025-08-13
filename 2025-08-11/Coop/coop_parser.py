import requests
from mongoengine import connect
import logging
import json
from parsel import Selector
from pymongo import MongoClient
from coop_items import ProductItem, FailedItem
from settings import (
    MONGO_URI, DB_NAME, headers,
    CRAWLER_COLLECTION, PARSE_COLLECTION, cookies
)


class Parser:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
        self.client = MongoClient(MONGO_URI)
        self.crawler_collection = self.client[DB_NAME][CRAWLER_COLLECTION]
        self.parser_collection = self.client[DB_NAME][PARSE_COLLECTION]
        self.session = self.reset_session()
    
    def reset_session(self):
        session = requests.Session()
        session.headers.update(headers)
        session.cookies.update(cookies)

        return session

    def start(self):
        links = self.crawler_collection.find()

        request_count = 0
        for link in links:
            link = link.get("url","")


            if request_count >= 50:
                self.session = self.reset_session()
                request_count = 0

            response = self.session.get(link, timeout=10)
            request_count += 1

            if response.status_code == 200:
                self.parse_item(link,response)
            else:
                FailedItem(url=link, source = "parser").save()
                logging.error(f"Status code : {response.status_code}")

    def parse_item(self,link, response):

        sel = Selector(response.text)

        PRODUCT_NAME_XPATH = '//h1/text()'
        REVIEW_XPATH = '//span[@itemprop="reviewCount"]/text()'
        RATING_XPATH = '//div[@class="rating"]/span/text()'
        BREADCRUMB_XPATH = '//li[@class="breadCrumb__item"]/a/span/text()'
        BRAND_XPATH = '//span[@class="productBasicInfo__productMeta-value-item"]/span/text()'
        SELLING_PRICE_XPATH = '//p[@data-testauto="productprice"]/text()'
        REGULAR_PRICE_XPATH = '//p[contains(@class, "price-value-lead-price-old")]/text()'
        GRAMMAGE_QUANTITY_XPATH = '//span[@data-testauto="productweight"]/text()'
        GRAMMAGE_UNIT_XPATH = '//span[@data-testauto="productweight"]/following-sibling::text()'
        PERCENTAGE_DISCOUNT_XPATH = '//dt[contains(@id, "rebateText")]/text()'
        COUNTRY_XPATH = '//div[@data-testauto="productcountry"]/text()'
        JSON_XPATH = '//script[@type="application/ld+json" and contains(text(),"offers")]/text()'


        product_name = sel.xpath(PRODUCT_NAME_XPATH).get()
        review = sel.xpath(REVIEW_XPATH).get()
        rating = sel.xpath(RATING_XPATH).get()
        breadcrumb = sel.xpath(BREADCRUMB_XPATH).getall()
        brand = sel.xpath(BRAND_XPATH).get()
        selling_price = sel.xpath(SELLING_PRICE_XPATH).get()
        regular_price = sel.xpath(REGULAR_PRICE_XPATH).get()
        percentage_discount = sel.xpath(PERCENTAGE_DISCOUNT_XPATH).get()
        grammage_quantity = sel.xpath(GRAMMAGE_QUANTITY_XPATH).get()
        grammage_unit = sel.xpath(GRAMMAGE_UNIT_XPATH).get()
        country_of_origin  = sel.xpath(COUNTRY_XPATH).get()

        json_ld = sel.xpath(JSON_XPATH).get()
        
        data = json.loads(json_ld)
        image = data.get("image", "")
        image = f"https://{image[0].split("//",2)[-1]}"

        product_id = link.split("/")[-1]
        product_name = product_name.strip()
        rating = rating.split(":")[1].replace("of 5", "").strip() if rating else ""
        breadcrumb = " > ".join(breadcrumb)
        brand = brand.strip() if brand else ""
        selling_price = selling_price.strip() if selling_price else "0"
        regular_price = regular_price.strip() if regular_price else "0"
        grammage_quantity = grammage_quantity.strip() if grammage_quantity else ""
        grammage_unit = grammage_unit.strip() if grammage_unit else ""
        percentage_discount = percentage_discount.replace("%", "").strip() if percentage_discount else ""
        percentage_discount = (
            percentage_discount 
            if percentage_discount and percentage_discount.isdigit() 
            else ""
        )
        country_of_origin = country_of_origin.strip() if country_of_origin else ""

        
        item = {}

        item["pdp_url"] = link
        item["product_name"] = product_name
        item["product_id"] = product_id
        item["review"] = review
        item["rating"] = rating
        item["breadcrumb"] = breadcrumb
        item["brand"] = brand
        item["selling_price"] = selling_price
        item["regular_price"] = regular_price
        item["grammage_quantity"] = grammage_quantity
        item["grammage_unit"] = grammage_unit
        item["percentage_discount"] = percentage_discount
        item["country_of_origin"] = country_of_origin
        item["image"] = image

        logging.info(item)
        try:
            ProductItem(**item).save()
        except:
            pass



if __name__ == "__main__":
    parser = Parser()
    parser.start()
