import requests
from mongoengine import connect
import logging
from parsel import Selector
from pymongo import MongoClient
from styleunion_items import  FailedItem, ProductItem
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
                logging.info(f"Skipping already parsed: {link}")
                continue

            response = requests.get(link,headers=HEADERS)
            if response.status_code == 200:
                self.parse_item(link,response)
            else:
                product_item = FailedItem(url = link, source ="parser")
                product_item.save()
        
    
    def parse_item(self,link,response):
        sel = Selector(response.text)
        logging.info(link)

        PRODUCT_NAME_XPATH = '//h1[@class="product__section-title product-title"]/text()'
        REGULAR_PRICE_XPATH = '//span[@class="price-item price-item--regular"]/text()'
        COLOR_XPATH = '//span[@class="swatches__color-name"]/text()'
        SKU_XPATH = '//span[@id="variantSku"]/text()'
        SIZE_XPATH = '//label[@class="swatches__form--label"]/text()'
        CARE_INSTRUCTIONS_TEXT = (
            '//div[h3[text()="Wash and Care"]]/following-sibling::div/text()[normalize-space()]'
            '| //div[h3[text()="Wash and Care"]]/following-sibling::div/p/text()[normalize-space()]'
        )
        CARE_INSTRUCTIONS_LIST = (
            '//div[h3[text()="Wash and Care"]]/following-sibling::div/ul/li/text()'
            '| //div[h3[text()="Wash and Care"]]/following-sibling::div/li/text()'
        )
        FABRIC_TYPE_XPATH =  (
            '//strong[text()="Fabric Type:" or text()="Fabric:"]/following-sibling::text()'
            '| //li/b[text()="Fabric type:"]/following-sibling::text()'
        )
        PATTERN_XPATH = (
            '//strong[text()="Pattern:"]/following-sibling::text()'
            '| //b[text()="Pattern:"]/following-sibling::text()'
        )
        CLOTHING_FIT_XPATH = (
            '//strong[text()="Fit:" or text()="Fit Type:"]/following-sibling::text()'
            '| //b[text()="Fit:" or text()="Fit Type:"]/following-sibling::text()'
        )
        POCKET_XPATH = '//strong[text()="Pockets:"]/following-sibling::text()'

        SLEEVE_TYPE_XPATH = (
            '//strong[text()="Sleeve Type:"]/following-sibling::text()'
            '| //b[text()="Sleeve Type:"]/following-sibling::text()'
        )
        COLLAR_TYPE_XPATH = (
            '//strong[contains(text(),"Neck") or contains(text(), "Collar")]/following-sibling::text()'
            '| //b[contains(text(),"Neck") or contains(text(), "Collar")]/following-sibling::text()'
        )
        CLOATHING_LENGTH_XPATH = (
            '//b[text()="Length:"]/following-sibling::text()'
            '| //strong[text()="Length:"]/following-sibling::text()'
        )

        RATING_XPATH = '//div[@class="jdgm-prev-badge"]/@data-average-rating'
        REVIEW_XPATH = '//div[@class="jdgm-prev-badge"]/@data-number-of-reviews'
        DESCRIPTION_XPATH = (
            '//h3[text()="Description"]/following::div[contains(@class,"acc__panel")]/text()[normalize-space()]'
            '| //h3[text()="Description"]/following::div[contains(@class,"acc__panel")]//p//text()[normalize-space()]'
        )
        IMAGE_XPATH = '//div[@class="box-ratio "]/img[@class="js-thumb-item-img"]/@src'

        product_name = sel.xpath(PRODUCT_NAME_XPATH).get()
        regular_price = sel.xpath(REGULAR_PRICE_XPATH).get() 
        color = sel.xpath(COLOR_XPATH).getall()
        sku = sel.xpath(SKU_XPATH).get()
        size = sel.xpath(SIZE_XPATH).getall()
        care_instructions = sel.xpath(CARE_INSTRUCTIONS_TEXT).get()
        fabric_type = sel.xpath(FABRIC_TYPE_XPATH).get()
        pattern = sel.xpath(PATTERN_XPATH).get()
        clothing_fit = sel.xpath(CLOTHING_FIT_XPATH).get()
        pocket = sel.xpath(POCKET_XPATH).get()
        sleeve_type = sel.xpath(SLEEVE_TYPE_XPATH).get()
        collar_type = sel.xpath(COLLAR_TYPE_XPATH).get()
        product_description = sel.xpath(DESCRIPTION_XPATH).get()
        images = sel.xpath(IMAGE_XPATH).getall()
        clothing_length = sel.xpath(CLOATHING_LENGTH_XPATH).get()

        rating = sel.xpath(RATING_XPATH).get()
        review = sel.xpath(REVIEW_XPATH).get()

        if not care_instructions:
            care_instructions = sel.xpath(CARE_INSTRUCTIONS_LIST).getall()
            care_instructions = " ".join(care_instructions)
        else:
            care_instructions = care_instructions.strip() 
        
        regular_price = regular_price.strip().replace("₹","").replace(",","") if regular_price else ""
        size = [i.strip() for i in size if i.strip()]
        fabric_type = fabric_type.strip() if fabric_type else ""
        pattern = pattern.strip() if pattern else ""
        pocket = pocket.strip() if pocket else ""
        clothing_fit = clothing_fit.strip() if clothing_fit else ""
        sleeve_type = sleeve_type.strip() if sleeve_type else ""
        collar_type = collar_type.strip() if collar_type else ""
        product_description = (
            product_description.strip().replace("\n","").replace("*","")
            if product_description else ""
        )
        images = [f"https:{image}" for image in images]
        clothing_length = clothing_length.strip() if clothing_length else ""
    

        item = {}

        item["pdp_url"] = link
        item["product_name"] = product_name
        item["regular_price"] = regular_price
        item["color"] = color
        item["sku"] = sku
        item["size"] = size
        item["care_instructions"] = care_instructions
        item["fabric_type"] = fabric_type
        item["rating"] = rating
        item["review"] = review
        item["pattern"] = pattern
        item["pocket"] = pocket
        item["clothing_fit"] = clothing_fit
        item["sleeve_type"] = sleeve_type
        item["collar_type"] = collar_type
        item["clothing_length"] = clothing_length
        item["product_description"] = product_description
        item["images"] = images

        logging.info(item)
        product_item = ProductItem(**item)
        product_item.save()
        



if __name__ == "__main__":
    parser_obj = Parser()
    parser_obj.start()
