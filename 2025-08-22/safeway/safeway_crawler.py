import requests
import logging
from pymongo import MongoClient
from settings import HEADERS, DB_NAME, MONGO_URI, MONGO_COLLECTION_CATEGORY
from safeway_items import ProductUrlItem, FailedItem
from mongoengine import connect
from parsel import Selector
import json



class Crawler:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
        self.client = MongoClient(MONGO_URI)
        self.category_collection = self.client[DB_NAME][MONGO_COLLECTION_CATEGORY]
        
    
    def start(self):
        for category_url in self.category_collection.find():
            category_url = category_url.get("url","")
            logging.info(category_url)
            
            cookies = {
                'abs_gsession': '%7B%22info%22%3A%7B%22COMMON%22%3A%7B%22Selection%22%3A%22user%22%2C%22preference%22%3A%22Delivery%22%2C%22userType%22%3A%22G%22%2C%22zipcode%22%3A%2295605%22%2C%22banner%22%3A%22safeway%22%2C%22siteType%22%3A%22C%22%2C%22customerType%22%3A%22%22%2C%22resolvedBy%22%3A%22zipcode%22%7D%2C%22J4U%22%3A%7B%22zipcode%22%3A%2295605%22%2C%22storeId%22%3A%222684%22%7D%2C%22SHOP%22%3A%7B%22zipcode%22%3A%2295605%22%2C%22storeId%22%3A%222684%22%7D%7D%7D',
                'SWY_SYND_USER_INFO': '%7B%22storeAddress%22%3A%22%22%2C%22storeZip%22%3A%2295605%22%2C%22storeId%22%3A%222684%22%2C%22preference%22%3A%22Delivery%22%2C%22xDTags%22%3A%22captcha_cleared%22%7D',
                'SWY_SHARED_SESSION_INFO': '%7B%22info%22%3A%7B%22COMMON%22%3A%7B%22userType%22%3A%22G%22%2C%22zipcode%22%3A%2295605%22%2C%22banner%22%3A%22safeway%22%2C%22preference%22%3A%22Delivery%22%2C%22Selection%22%3A%22user%22%2C%22xDTags%22%3A%22captcha_cleared%22%2C%22wfcStoreId%22%3A%225799%22%2C%22userData%22%3A%7B%7D%2C%22grsSessionId%22%3A%224c8c5c39-f65a-49d5-8acb-873e2e0ca3d2%22%2C%22siteType%22%3A%22C%22%2C%22customerType%22%3A%22%22%2C%22resolvedBy%22%3A%22zipcode%22%7D%2C%22J4U%22%3A%7B%22storeId%22%3A%222684%22%2C%22zipcode%22%3A%2295605%22%2C%22userData%22%3A%7B%7D%7D%2C%22SHOP%22%3A%7B%22storeId%22%3A%222684%22%2C%22zipcode%22%3A%2295605%22%2C%22userData%22%3A%7B%7D%7D%7D%7D',
                'reese84': '3:PecNWgNXrubOR24PirK9qQ==:yfGKfO6VBh7RICmEqJJGoR19zOpacgW8BMhgyvQvrSseWZkFCK9HRoACy6w6IRnoLADL/Rvox7o2DcGsBHsmODCrKuqKxfeNkJuVUfTC1khk6mKg0d0dcDtkHBHWzMZgjAPAiNzrzNj6rp0DzzW52oRH9vjaQJhRc4btndFjzUPDpoSC0ohQidnakmHEmdKWLgr3cijudAoMbC0cfehCr15bo2CzsepNz3ti27RmWhhr6ZeDGxksMhDoerYKeAzSwMAuFiMPUzbPLiKyZTGaRfaVa51At/4Rj2WvPxjx4fX209vB8nVjw8wKl5ymSNNG7P1L9rWXnKGBfSS9aahj1qP5mh3q11vJftEgHKQZu0FEzt8OD8y1M1HsGMIji0wjvuF7Hsnz5d0FA6PK/K9B5ELsUYei3yHdOh+Fi6umfRHAgNxG2xpl0ee1wvfxhyX1XgJNkqBx9y1XYlA4msO+fahxCUqmizk2qZORy8YlnhZjTiU2MjdKSOrm9OG3yBSQuMpi+2pOT/vH/VFRKNwvU1941U5gF3PnDhGZeP+1m8vDaeZCU0O/MsjXN+ueAAXk:GWlVd45l53UDmVASgfbpY9OhKwYnRG5AD011m3m07d0=',
            }
            
            page_no = 1
            
            while True:
                category_url = f"{category_url}?sort=&page={page_no}&loc=2684"
                response = requests.get(url=category_url, headers=HEADERS, cookies=cookies)
                
                if response.status_code == 200:
                    sel = Selector(response.text)
                    pdp_urls = sel.xpath('//a[contains(@href, "/product-details")]/@href').getall()
                    load_more = sel.xpath('//a[contains(text(), "Load more")]/@href').get()
                    
                    if not load_more:
                        break
                    
                    for url in set(pdp_urls):
                        logging.info(url)
                        # try:
                        #     ProductUrlItem(url=url).save()
                        # except:
                        #     pass
                    
                    page_no += 1
                    
                else:
                    logging.error(f"Status code : {response.status_code}")
                    FailedItem(url=category_url, source = "crawler").save()
                    break
                    
            
        
        
if __name__ == "__main__":
    crawler = Crawler()
    crawler.start()