import requests
from mongoengine import connect
import logging
from parsel import Selector
from pymongo import MongoClient
from gall_items import  FailedItem, ProductItem
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

        PRODUCT_NAME_XPATH = "//h1[@class='pdp-info_name']/text()"
        REGULAR_PRICE_XPATH = 'concat(//span[@class="price-value "]/text(), //span[@class="price-value "]/@data-decimals)'
        PRODUCT_DESCRIPTION = "//div[@id='product-description']/p/text()"
        BREADCRUMB_XPATH = "//a[@class='breadcrumb__label is--link']/span/text()"
        RATING_XPATH = "//span[@class='rating_label']/text()"
        REVIEW_XPATH = "//span[@class='rating_label']/@data-count"
        IMAGE_XPATH = "//figure[@class='a-image image-contain pdp-info_image']/img/@src"
        ALCHOLE_PER_XPATH = "//td[text()='Alcoholpercentage']/following-sibling::td/text()"
        INGREDIENT_XPATH = "//td[text()='Ingrediënten']/following-sibling::td/text()"
        ALLERGENS_XPATH = "//td[text()='Allergie-informatie']/following-sibling::td/text()"
        ALCHOLE_VOL_XPATH = "//td[text()='Inhoud']/following-sibling::td/text()"
        INSTOCK_XPATH = '//div[contains(@class, "product-online-availability")]/text()'
        NUTRITIONS_XPATH = '//div[@class="product-nutritional-values"]//tr[not(@class="product-nutritional-serving")]'

        product_name = sel.xpath(PRODUCT_NAME_XPATH).get()
        regular_price = sel.xpath(REGULAR_PRICE_XPATH).get()
        product_description = sel.xpath(PRODUCT_DESCRIPTION).get()
        breadcrumb = sel.xpath(BREADCRUMB_XPATH).getall()
        rating = sel.xpath(RATING_XPATH).get()
        review = sel.xpath(REVIEW_XPATH).get()
        image = sel.xpath(IMAGE_XPATH).get()
        alchole_percentage = sel.xpath(ALCHOLE_PER_XPATH).get()
        ingredient = sel.xpath(INGREDIENT_XPATH).get()
        allergens = sel.xpath(ALLERGENS_XPATH).get()
        alchol_by_volume = sel.xpath(ALCHOLE_VOL_XPATH).get()
        instock = sel.xpath(INSTOCK_XPATH).get()
        

        instock = True if instock == "Online op voorraad" else False

        nutritions  = {}
        table_rows = sel.xpath(NUTRITIONS_XPATH)
        for row in table_rows:
            key = row.xpath('./td[1]/text()').get()
            value = row.xpath('./td[2]/text()').get()
            nutritions[key] = value

        item = {}

        item["pdp_url"] = link
        item["product_name"] = product_name
        item["product_description"] = product_description
        item["regular_price"] = regular_price
        item["breadcrumb"] = breadcrumb
        item["rating"] = rating
        item["review"] = review
        item["image"] = image
        item["alchole_percentage"] = alchole_percentage
        item["ingredient"] = ingredient
        item["allergens"] = allergens
        item["alchol_by_volume"] = alchol_by_volume
        item["instock"] = instock

        logging.info(item)

        try:
            ProductItem(**item).save()
        except:
            pass



if __name__ == "__main__":
    parser = Parser()
    parser.start()
