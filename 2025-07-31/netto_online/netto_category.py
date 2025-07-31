from curl_cffi import requests
import logging
from parsel import Selector
from settings import HEADERS, MONGO_URI, DB_NAME, BASE_URL
from mongoengine import connect
from netto_items import CategoryItem


class Category:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")

    def start(self):
        
        response = requests.get(BASE_URL , headers= HEADERS, impersonate="chrome")
        if response.status_code == 200:
            sel = Selector(response.text)

            category_urls = sel.xpath('//a[contains(@class, "inner-list__item__link")]/@href').getall()

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
