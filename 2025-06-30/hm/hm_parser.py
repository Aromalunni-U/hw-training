import requests
from mongoengine import connect
import logging
from parsel import Selector
from pymongo import MongoClient
from hm_items import  FailedItem, ProductItem
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
                
    
    def parse_item(self,link,response):
        sel = Selector(response.text)

        PRODUCT_NAME_XPATH = '//h1[@class="fe9348 bdb3fa d582fb"]/text()'
        REGULAR_PRICE_XPATH = '//span[@class="e70f50 d7cab8 d9ca8b"]/text()'
        ART_NUMBER_XPATH = '//p[contains(text(), "Art. No.")]/text()'
        COMPOSITION_XPATH = '//span[@class="e95b5c f8c1e9 efef57"]/text()'
        CLOTHING_LENGTH = '//dt[contains(text(), "Length")]/following-sibling::dd/text()'
        CLOTHING_FIT = '//dt[contains(text(), "Fit")]/following-sibling::dd/text()'
        COUNTRY_OF_ORGIN_XPATH = '//dt[contains(text(), "Country of production")]/following-sibling::dd/text()'
        NECK_STYLE = '//dt[contains(text(), "Neckline")]/following-sibling::dd/text()'
        STYLE_XPATH = '//dt[contains(text(), "Style")]/following-sibling::dd/text()'
        CARE_INSTRUCTION = '//h3[contains(text(), "Care instructions")]/following-sibling::ul/li/text()'
        SIZE_XPATH = '//dt[contains(text(), "Size")]/following-sibling::dd/text()'
        COLOR_XPATH = '//dt[contains(text(), "Description")]/following-sibling::dd/text()'
        SLEEVE_LENGTH = '//dt[contains(text(), "Sleeve Length")]/following-sibling::dd/text()'
        IMAGE_XPATH = '//ul[@data-testid="grid-gallery"]//img/@srcset'

        product_name = sel.xpath(PRODUCT_NAME_XPATH).get()
        regular_price = sel.xpath(REGULAR_PRICE_XPATH).get()
        art_number = sel.xpath(ART_NUMBER_XPATH).getall()
        material_composition = sel.xpath(COMPOSITION_XPATH).get()
        clothing_length = sel.xpath(CLOTHING_LENGTH).get()
        clothing_fit = sel.xpath(CLOTHING_FIT).get()
        country_of_origin = sel.xpath(COUNTRY_OF_ORGIN_XPATH).get()
        neck_style = sel.xpath(NECK_STYLE).get()
        style = sel.xpath(STYLE_XPATH).get()
        care_instruction = sel.xpath(CARE_INSTRUCTION).getall()
        size = sel.xpath(SIZE_XPATH).getall()
        color  =sel.xpath(COLOR_XPATH).get()
        sleeve_length_style = sel.xpath(SLEEVE_LENGTH).get()
        images = sel.xpath(IMAGE_XPATH).getall()


        regular_price = (
                regular_price.replace("Rs.","").replace(",","").strip()
                if regular_price else ""
            )
        art_number = "".join(art_number).split(":")[-1].strip() if art_number else ""
        neck_style = neck_style.strip() if neck_style else ""
        style = style.strip() if style else ""
        care_instruction = ", ".join(care_instruction) if care_instruction else ""
        size = [s.split(":")[0] for s in size]
        color = color.split(",")[0] if color else ""
        sleeve_length_style = sleeve_length_style.strip() if sleeve_length_style else ""
        images = [img.split(",")[-1].split()[0]  for img in images]

        item = {}

        item["pdp_url"] = link
        item["product_name"] = product_name 
        item["regular_price"] = regular_price 
        item["art_number"] = art_number
        item["material_composition"] = material_composition 
        item["clothing_length"] = clothing_length 
        item["clothing_fit"] = clothing_fit
        item["country_of_origin"] = country_of_origin 
        item["neck_style"] = neck_style
        item["style"] = style 
        item["care_instruction"] = care_instruction
        item["color"] = color 
        item["sleeve_length_style"] = sleeve_length_style
        item["images"] = images
        
        logging.info(item)
        product_item = ProductItem(**item)
        product_item.save()



if __name__ == "__main__":
    parser_obj = Parser()
    parser_obj.start()