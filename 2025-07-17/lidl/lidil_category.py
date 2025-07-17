import requests
import logging
from parsel import Selector
from settings import HEADERS, MONGO_URI, DB_NAME, BASE_URL
from mongoengine import connect
from lidil_items import CategoryItem


class Category:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")

    def start(self):
        
        response = requests.get(BASE_URL , headers= HEADERS)
        if response.status_code == 200:
            sel = Selector(response.text)

            category_links = sel.xpath('//li[contains(@class, "ux-base-slider__slide")]//a[contains(@class, "ACategoryOverviewSlider__Link")]/@href').getall()

            full_links = [f"https://www.lidl.nl{link}" for link in category_links]

            for url in full_links:
                res = requests.get(url, headers=HEADERS)

                if res.status_code == 200:

                    sel = Selector(res.text)
                    category_url = sel.xpath('//a[contains(@href, "alle-producten")]/@href').get()

                    category_url = category_url.strip() if category_url else url
                    logging.info(category_url)

                    try:
                        CategoryItem(url = category_url).save()
                    except:
                        pass   

                else:
                    logging.error(f"Status code : {res.status_code}")


   

if __name__ == "__main__":
    category = Category()
    category.start()
