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
        'datadome': '2mSnKqADcMbwDwWM3vW~uINMeP0cVG3X7FF5j8ZoQVzpfnJGMCXFc06a2QR4ZAl9C1WDV_MncZlsIw0VWSbO18w4skZobLB9UegmIOPNH_UqGbfC88nI_2T0O4bAp__K'
        }

        session = requests.Session()

        response = session.get(BASE_URL, headers=headers,cookies=cookies,timeout=10)
    
        if response.status_code == 200:
            sel = Selector(response.text)

            category_urls = sel.xpath('//a[@data-navigation-category-code]/@href').getall()
            category_urls = [f"https://www.coop.ch{url}" for url in category_urls if "/c/" in url]

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
