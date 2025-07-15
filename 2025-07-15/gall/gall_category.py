import requests
import logging
from parsel import Selector
from settings import HEADERS, BASE_URL, MONGO_URI, DB_NAME
from mongoengine import connect
from gall_items import CategoryItem



class Category:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
    
    def start(self):
        response = requests.get(BASE_URL, headers = HEADERS)
        if response.status_code == 200:
            sel = Selector(response.text)
            category_urls = sel.xpath("//button[contains(text(), 'Alle ')]/@data-action").getall()

            category_urls = [f"https://www.gall.nl{url}" for url in category_urls]

            for category_url in category_urls:
                logging.info(category_url)

                try:
                    CategoryItem(url = category_url).save()
                except:
                    pass



if __name__ == "__main__":
    category = Category()
    category.start()