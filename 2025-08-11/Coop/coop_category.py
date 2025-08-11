import requests 
import logging
from parsel import Selector
from settings import  MONGO_URI, DB_NAME, BASE_URL, headers
from mongoengine import connect
from coop_items import CategoryItem


class Category:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")

    def start(self):
        
        cookies = {
        'datadome': '1~YZyQTI1fW9TJncY9NnIqrboYiuFA4R5wkf2AhJpBj38wDin6UyxI7EZyUUk3Qfu4jRDDJC4G48KGoM4BE9Mqr_O1tSGREzEwP7VfpsKCoGJusDdt2b6MIK5m0TNJZ7'
        }

        session = requests.Session()

        response = session.get(BASE_URL, headers=headers,cookies=cookies,timeout=10)
    
        if response.status_code == 200:
            sel = Selector(response.text)

            category_urls = sel.xpath('//a[@data-page-type="product-list"]/@href').getall()
            category_urls = [f"https://www.coop.ch{url}" for url in category_urls]

            for url in category_urls:
                logging.info(url)
                try:
                    CategoryItem(url = url).save()
                except:
                    pass 
        else:
            logging.error(f"Status code {response.status_code}")




if __name__ == "__main__":
    category = Category()
    category.start()
