import requests
from parsel import Selector
import logging
from settings import BASE_URL, DB_NAME, MONGO_URI, HEADERS
from mongoengine import connect
from styleunion_items import ProductUrlItem, FailedItem



class Crawler:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
    
    def start(self):

        page_no = 1  
        next_page = f"{BASE_URL}?page={page_no}"

        while next_page:
            response = requests.get(url=next_page, headers=HEADERS)
            if response.status_code == 200:
                products_found = self.parse_item(response)
                
                if not products_found:
                    break

                page_no += 1
                next_page = f"{BASE_URL}?page={page_no}"

            else:
                logging.error(f"Status code: {response.status_code}")
                FailedItem(url=next_page, source="crawler").save()
                break
    
    def parse_item(self,response):

        sel = Selector(response.text)

        PRODUCT_CARD_XPATH = '//div[starts-with(@id, "product-listing-")]'
        NO_RESULT_XPATH = '//span[@class="rte" and contains(text(), "No results.")]'
        PDP_URL_XPATH = './/div[@class="product-info"]/a/@href'
        PRODUCT_NAME_XPATH  = './@data-alpha'
        REGULAR_PRICE_XPATH = './/span[@class="price-item price-item--regular"]/text()'
        IMAGE_XPATH = './/div[@class="box-ratio "]/img/@src'

        product_card = sel.xpath(PRODUCT_CARD_XPATH)
        if not product_card or sel.xpath(NO_RESULT_XPATH):
            return False

        for card in product_card:
            pdp_url = card.xpath(PDP_URL_XPATH).get()
            
            if "/collections/womens-tops/" not in pdp_url:
                continue

            product_name = card.xpath(PRODUCT_NAME_XPATH).get()
            regular_price = card.xpath(REGULAR_PRICE_XPATH).get()
            image = card.xpath(IMAGE_XPATH).get()

            pdp_url = f"https://styleunion.in{pdp_url}"
            regular_price = (
                regular_price.replace("from ", "").replace(",", "").replace("₹", "").strip()
                if regular_price else ""
            )
            image = f"https:{image}" if image else ""

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

            
