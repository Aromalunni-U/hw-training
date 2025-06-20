import requests
import logging
from settings import HEADERS, MONGO_URI, DB_NAME, BASE_URL
from parsel import Selector
from mmlafleur_items import CategoryItem
from urllib.parse import urljoin
from mongoengine import connect


class Category:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")

    def start(self):
        response = requests.get(BASE_URL,headers=HEADERS)
        sel = Selector(response.text)
        category_urls = sel.xpath(
             '//div[a[@class="MegaMenu__Title" and text()="Categories"]]/ul[@class="Linklist"]/li/a/@href').getall()
        
        for url in category_urls:
                full_url = urljoin(BASE_URL,url)
                logging.info(full_url)
                category_item = CategoryItem(url=url)
                category_item.save()
            

if __name__ == "__main__":
    category = Category()
    category.start()