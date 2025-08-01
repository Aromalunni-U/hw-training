from curl_cffi import requests
from mongoengine import connect
import json
import logging
from parsel import Selector
from pymongo import MongoClient
from netto_items import  FailedItem, ProductItem
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
                logging.error(f"Status code {response.status_code}")
                FailedItem(url = link, source ="parser").save()
    
    def parse_item(self,link, response):
        logging.info(link)
        sel = Selector(response.text)


        PROMO_DESCRIPTION_XPATH = '//span[contains(@class, "tc-product-pricesaving")]/text()'
        PRICE_XPATH = '//div[@class="product__price__label"]//span[contains(@class, "product__strike-price")]//span[not(contains(@class, " "))]/text()'
        INSTOCK_XPATH = '//span[contains(@class, "product-availability__text")]/text()'
        PRODUCT_DESCRIPTION_XPATH = '//div[contains(@class, "tc-product-description")]//text()'
        BREADCRUMB_XPATH = '//ol[contains(@class, "breadcrumb")]//span[@itemprop="name"]/text()'

        promotion_description = sel.xpath(PROMO_DESCRIPTION_XPATH).get()
        price_was = sel.xpath(PRICE_XPATH).getall()
        instock = sel.xpath(INSTOCK_XPATH).get()
        breadcrumb = sel.xpath(BREADCRUMB_XPATH).getall()
        product_description = sel.xpath(PRODUCT_DESCRIPTION_XPATH).getall()

        json_ld = sel.xpath('//script[@type="application/ld+json"]/text()').get()

        try:
            json_ld = json_ld.replace('\n', '').replace('\r', '').strip()
            data = json.loads(json_ld)
        except:
            FailedItem(url=link, source="parser-json").save()
            return

        offers = data.get("offers", {})
        aggregate_rating = data.get("aggregateRating", {})

        product_name = data.get("name", "")
        brand = data.get("brand",{}).get("name", "")
        selling_price = offers.get("price", "")
        currency = offers.get("priceCurrency", "")
        rating = aggregate_rating.get("ratingValue", "")
        review = aggregate_rating.get("reviewCount", "")
        image = data.get("image", "")

        instock = True if instock and instock.lower().strip() == "auf lager" else False
        product_description =(
            " ".join(product_description).replace("\n","").replace("\xa0", "").strip() 
            if product_description else ""
        )
        price_was = ( 
            "".join(price_was).replace("\n","").replace("*","").replace("–","").strip()
            if price_was else 0 
        )
        breadcrumb = " > ".join(breadcrumb[:-1])
        promotion_description = promotion_description.replace("\xa0", "").strip() if promotion_description else ""
        product_id = link.split("/")[-1].split("?")[0]
        image = image.split("?")[0]

        item = {}

        item["pdp_url"] = link
        item["product_id"] = product_id
        item["product_name"] = product_name
        item["brand"] = brand
        item["selling_price"] = selling_price
        item["price_was"] = price_was
        item["currency"] = currency
        item["rating"] = rating
        item["review"] = review
        item["image"] = image
        item["instock"] = instock
        item["breadcrumb"] = breadcrumb
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
