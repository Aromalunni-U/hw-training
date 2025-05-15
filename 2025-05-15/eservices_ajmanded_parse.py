from curl_cffi import requests
from parsel import Selector
from settings import *
import logging
from tqdm import tqdm
from eservices_ajmanded_crawler import Crawler
from pymongo import MongoClient


client = MongoClient(MONGO_URI)  
db = client[DB_NAME] 
crawler_collection = db[CRAWLER_COLLECTION] 
parser_collection = db[PARSE_COLLECTION]

def Parser(links):
    try:
        for link in tqdm(links):
            response =  requests.get(link,impersonate="chrome", timeout=60)
            if response.status_code == 200:
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
                area_xpath = "//h5[text()='Contact Details']/following-sibling::ul[1]/li[2]/text()"

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

                yield {
                    "real_estate_link":link,
                    "license_number":license_number,
                    "license_type":license_type,
                    "legal_form":legal_form,
                    "arabic_trade_name":arabic_trade_name,
                    "english_trade_name":english_trade_name,
                    "license_start_date":license_start_date,
                    "license_expiry_date":license_expiry_date,
                    "activities":activities,
                    "est_banning_status":est_banning_status,
                    "area":area
                }
            else:
                logging.error(response.status_code) 
    except Exception as e:
        logging.error(f"An error occured: {e}")



estate_links = Crawler(BASE_URL)

if estate_links:
    crawler_collection.insert_many([{"real_estate_link": link} for link in estate_links])

data = list(Parser(estate_links))

if data:
    parser_collection.insert_many(data)
    logging.info("Completed successfully")

