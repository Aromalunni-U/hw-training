from curl_cffi import requests
from parsel import Selector
from settings import *
import logging
from pymongo import MongoClient


class Parser:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        self.crawler_collection = self.db[CRAWLER_COLLECTION]
        self.parser_collection = self.db[PARSE_COLLECTION]


    def start(self):
        links = self.crawler_collection.find()
        for link in links:
            link = link.get("real_estate_link")
            response =  requests.get(link,impersonate="chrome", timeout=60)
            if response.status_code == 200:
                self.parse_item(link,response)
    
    def parse_item(self, url, response):

        sel = Selector(response.text)

        license_number_xpath = "//ul/li[@class='res-item'][position()=1]/text()"
        license_type_xpath = "//ul/li[@class='res-item'][position()=2]/text()"
        legal_form_xpath = "//ul/li[@class='res-item'][position()=3]/text()"
        arabic_trade_name_xpath =  "//ul/li[@class='res-item'][position()=4]/text()"
        english_trade_name_xapth = "//ul/li[@class='res-item'][position()=5]/text()"
        license_start_date_xpath = "//ul/li[@class='res-item'][position()=6]/text()"
        license_expiry_date_xpath = "//ul/li[@class='res-item'][position()=7]/text()"
        activities_xpath = "//h5[text()='Activities']/following-sibling::ul[1]/li[@class='res-item']/text()"
        est_banning_status_xpath = "//h5[text()='Contact Details']/following-sibling::ul[1]/li[@class='res-item']/text()"
        area_xpath = "//li[span[text()='Area']]/text()"

        license_number = sel.xpath(license_number_xpath).get()
        license_type = sel.xpath(license_type_xpath).get()
        legal_form = sel.xpath(legal_form_xpath).get()
        arabic_trade_name = sel.xpath(arabic_trade_name_xpath).get()
        english_trade_name = sel.xpath(english_trade_name_xapth).get()
        license_start_date = sel.xpath(license_start_date_xpath).get()
        license_expiry_date = sel.xpath(license_expiry_date_xpath).get()
        activities = sel.xpath(activities_xpath).getall()
        est_banning_status = sel.xpath(est_banning_status_xpath).get()
        area = sel.xpath(area_xpath).get()

        license_type = license_type.strip() if license_type else "not available"
        legal_form = legal_form.strip() if legal_form else "not available"
        activities = activities if activities else "not available"
        est_banning_status = est_banning_status if est_banning_status else "not available"

        item = {}

        item["real_estate_link"] = url
        item["license_number"] = license_number
        item["license_type"] = license_type
        item["legal_form"] = legal_form
        item["arabic_trade_name"] = arabic_trade_name
        item["english_trade_name"] = english_trade_name
        item["license_start_date"] = license_start_date
        item["license_expiry_date"] = license_expiry_date
        item["activities"] = activities
        item["est_banning_status"] = est_banning_status
        item["area"] = area

        logging.info(item)
        self.parser_collection.insert_one(item)
        
 

parser = Parser()
parser.start()