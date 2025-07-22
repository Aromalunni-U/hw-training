import requests
import logging
from homedepot_items import  FailedItem, ProductUrlItem
from mongoengine import connect
from pymongo import MongoClient
from parsel import Selector
from settings import HEADERS, DB_NAME, MONGO_URI, CRAWLER_COLLECTION
import json



class Crawler:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
    
    def start(self):
        CATEGORY_URL = "https://www.homedepot.com/b/Cleaning/N-5yc1vZbqsi?catStyle=ShowProducts"
        CATEGORY_URL = "https://www.homedepot.com/b/Cleaning-Cleaning-Products/Pick-Up-Today/N-5yc1vZcb33Z1z175a5"

        page = 0

        while True:
            url = f"{CATEGORY_URL}&Nao={page}"

            response = requests.get(url, headers= HEADERS)

            if response.status_code == 200:
                sel = Selector(response.text)

                pdp_links = sel.xpath('//div[@data-testid="product-pod"]/a/@href').getall()
                pdp_links = [f"https://www.homedepot.com{link}" for link in pdp_links]

                json_text = sel.xpath('//script[@id="thd-helmet__script--browseSearchStructuredData"]/text()').get()
                if not json_text:
                    break
                data = json.loads(json_text)

                for block in data:
                    entity = block.get("mainEntity")
                    if entity and "offers" in entity:
                        offers = entity["offers"]
                        products = offers.get("itemOffered", [])
                        for item in products:
                            offer = item.get("offers")
                            if offer and "url" in offer:
                                pdp_links.append(offer["url"])

                if not pdp_links:
                    break

                for url in pdp_links:
                    logging.info(url)
                    try:
                        ProductUrlItem(url=url).save()
                    except:
                        pass
        
                page += 24
            else:
                logging.error(f"Status code {response.status_code}")
                FailedItem(url = url, source = "crawler").save()


if __name__ == "__main__":
    crawler = Crawler()
    crawler.start()