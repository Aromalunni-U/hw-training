import requests
from mongoengine import connect
import logging
from parsel import Selector
from pymongo import MongoClient
from westside_items import  FailedItem, ProductItem
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

        PRODUCT_NAME_XPATH = '//div[@class="product__title"]/h1/text()'
        REGULAR_PRICE_XPATH = '//span[@class="price-item price-item--regular"]/text()'
        BRAND_XPATH = '//div[@class="pdptitle"]/p/text()'
        COUNTRY_XPATH = '//b[contains(text(), "Country Of Origin")]/following-sibling::text()'
        PRODUCT_DESCRIPTION_XPATH = '//div[@class="features_discription"][normalize-space()]/p/text()'
        CARE_INSTRUCTION_XPATH = '//b[contains(text(), "Care Instruction")]/following-sibling::text()'
        MATERIAL_COMPOSITION_XPATH = '//b[contains(text(), "Fabric Composition")]/following-sibling::text()'
        CLOTHING_FIT_XPATH = '//b[contains(text(), "Fit")]/following-sibling::text()'
        IMAGE_XPATH = '//div[contains(@class, "product__media")]/img/@src'
        COLOR_XPATH = '//div[@class="tooltip"]/text()'
        BREADCCRUMB_XPATH = '//a[@class="breadcrumbs__link"]/text()'
        SKU_XPATH  = '//b[contains(text(), "SKU")]/following-sibling::text()'
        SIZE_XPATH ="//label[@class='product_clr_variant' and @id='pdp-variant']/text()"

        product_name = sel.xpath(PRODUCT_NAME_XPATH).get()
        regular_price = sel.xpath(REGULAR_PRICE_XPATH).get()
        brand = sel.xpath(BRAND_XPATH).get()
        country_of_origin = sel.xpath(COUNTRY_XPATH).get()
        description = sel.xpath(PRODUCT_DESCRIPTION_XPATH).get()
        care_instructions = sel.xpath(CARE_INSTRUCTION_XPATH).get()
        material_composition = sel.xpath(MATERIAL_COMPOSITION_XPATH).get()
        clothing_fit = sel.xpath(CLOTHING_FIT_XPATH).get()
        images = sel.xpath(IMAGE_XPATH).getall()
        color = sel.xpath(COLOR_XPATH).getall()
        breadcrumb = sel.xpath(BREADCCRUMB_XPATH).getall()
        sku = sel.xpath(SKU_XPATH).get()
        size = sel.xpath(SIZE_XPATH).getall()

        regular_price = regular_price.replace("₹", "").strip() if regular_price else ""
        brand = brand.strip() if brand else ""
        country_of_origin = country_of_origin.strip() if country_of_origin else ""
        description = description.strip() if description else ""
        care_instructions = care_instructions.strip() if care_instructions else ""
        material_composition = material_composition.strip() if material_composition else ""
        clothing_fit = clothing_fit.strip() if clothing_fit else ""
        images = [f"https:{img.split("?")[0]}" for img in set(images)]
        breadcrumb = " > ".join(breadcrumb) if breadcrumb else ""
        size = [i.strip() for i in size]
        sku = sku.strip() if sku else ""

        item = {}

        item["pdp_url"] = link
        item["product_name"] = product_name
        item["regular_price"] = regular_price
        item["brand"] = brand 
        item["country_of_origin"] = country_of_origin
        item["product_description"] = description
        item["care_instructions"] = care_instructions
        item["material_composition"] = material_composition
        item["clothing_fit"] = clothing_fit
        item["images"] = images
        item["color"] = color
        item["breadcrumb"] = breadcrumb
        item["sku"] = sku
        item["size"] = size

        logging.info(item)

        try:
            ProductItem(**item).save()
        except:
            pass


if __name__ == "__main__":
    parser = Parser()
    parser.start()


