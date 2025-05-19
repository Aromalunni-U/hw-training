import logging
from parsel import Selector
from settings import MONGO_URI, DB_NAME,CRAWLER_COLLECTION, PARSE_COLLECTION
from pymongo import MongoClient
from curl_cffi import requests
from time import sleep


class Parser:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        self.crawler_collection = self.db[CRAWLER_COLLECTION]
        self.parser_collection = self.db[PARSE_COLLECTION]


    def start(self):
        links = self.crawler_collection.find()
        for link in links:
            link = link.get("links")
            response =  requests.get(link, impersonate="chrome", timeout=60)
            sleep(0.5)
            if response.status_code == 200:
                self.parse_item(link, response)

    def parse_item(self, url, response):

        sel = Selector(response.text)

        currency_xpath = "//span[@aria-label='Price']/text()"
        price_xpath = "//span[@aria-label='Price']/text()"
        beadroom_xpath = "//span[text()='Bedrooms']/following-sibling::span/text()"
        bathroom_xpath = "//span[text()='Bathrooms']/following-sibling::span/text()"
        furnished_xpath = "//span[text()='Furnished']/following-sibling::span/text()"
        area_xpath = "//span[text()='Area (m²)']/following-sibling::span/text()"
        location_xpath = "//span[@aria-label='Location']/text()"
        amenities_xpath = "//span[@class='c327b807']/text()"
        price_type_xpath = "//span[text()='Price Type']/following-sibling::span/text()"
        breadcrumb_xpath = "//a[@itemprop='item']/text()"
        description_xpath = "//div[@class='_472bfbef']/span/span/text()"
        image_xpath = "//img[@role='presentation' and @class='cf8850e1']/@src"

        currency = sel.xpath(currency_xpath).get()
        price = sel.xpath(price_xpath).get()
        beadroom = sel.xpath(beadroom_xpath).get()
        bathroom = sel.xpath(bathroom_xpath).get()
        furnished = sel.xpath(furnished_xpath).get()
        area = sel.xpath(area_xpath).get()
        location = sel.xpath(location_xpath).get()
        amenities = sel.xpath(amenities_xpath).getall()
        price_type = sel.xpath(price_type_xpath).get()
        breadcrumb = sel.xpath(breadcrumb_xpath).getall()
        description = sel.xpath(description_xpath).get()
        images = sel.xpath(image_xpath).getall()

        currency = currency.split()[0] if currency else ""
        price = price.split()[1] if price else ""
        beadroom = beadroom if beadroom else ""
        bathroom = bathroom if bathroom else ""
        furnished = furnished if furnished else ""
        price_type = price_type if price_type else ""
        breadcrumb = ">".join(breadcrumb)
        description = description.replace("\n"," ").strip() if description else ""

        item = {}

        item["link"] = url
        item["currency"] = currency
        item["price"] = price
        item["beadroom"] = beadroom
        item["bathroom"] = bathroom
        item["furnished"] = furnished
        item["area"] = area
        item["location"] = location
        item["amenities"] = amenities
        item["price_type"] = price_type
        item["breadcrumb"] = breadcrumb
        item["description"] = description
        item["images"] = images

        logging.info(item)
        self.parser_collection.insert_one(item)


parser = Parser()
parser.start()