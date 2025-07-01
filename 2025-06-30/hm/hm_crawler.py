import requests
from parsel import Selector
import logging
from settings import  DB_NAME, MONGO_URI, HEADERS
from mongoengine import connect
from hm_items import ProductUrlItem, FailedItem



class Crawler:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
    
    def start(self):
        page_no = 1

        while True:
            next_page_url = f"https://www2.hm.com/en_in/women/shop-by-product/tops.html?productTypes=Top&page={page_no}"
            
            logging.info(f"Page: {page_no} - {next_page_url}")

            response = requests.get(next_page_url, headers= HEADERS)
            if response.status_code == 200:
                products_found = self.parse_item(response)
                
                if not products_found:
                    break
            else:
                logging.error(f"Failed : {response.status_code}")
                FailedItem(url=next_page_url, source="crawler").save()
                break

            page_no += 1

        
    def parse_item(self, response):
        sel = Selector(response.text)

        PRODUCT_CARD_XPATH = '//article[@class="df8bcc"]'
        PDP_URLS_XPATH = './/a[@href and contains(@href, "productpage")]/@href'
        PRODUCT_NAME_XPATH = './/h2/text()'
        REGULAR_PRICE_XPATH = './/span[contains(@class, "cd6aee")]/text()'
        IMAGES_XPATH = './/img/@srcset'

        product_card = sel.xpath(PRODUCT_CARD_XPATH)
        if not product_card:
            return False
        
        for card in product_card:
            pdp_url = card.xpath(PDP_URLS_XPATH).get()
            product_name = card.xpath(PRODUCT_NAME_XPATH).get()
            regular_price = card.xpath(REGULAR_PRICE_XPATH).get()
            image = card.xpath(IMAGES_XPATH).get()

            regular_price = (
                regular_price.replace("Rs.","").replace(",","")
                if regular_price else ""
            )
            image = image.split(",")[-1].split()[0] if image else ""

            item = {}

            item["url"] = pdp_url
            item["product_name"] = product_name
            item["regular_price"] = regular_price
            item["image"] = image

            logging.info(item)
            data_item = ProductUrlItem(**item)
            data_item.save()

        return True


if __name__ == "__main__":
    crawler = Crawler()
    crawler.start()

            