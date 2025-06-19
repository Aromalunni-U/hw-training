import requests
import logging
from settings import HEADERS, MONGO_URI, DB_NAME, BASE_URL
from parsel import Selector
from almayaonline_items import ProductUrlItem, CategoryItem, FailedItem
from mongoengine import connect
from urllib.parse import urlparse


class Crawler:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
    
    def start(self):
        response = requests.get(BASE_URL,headers=HEADERS)
        sel = Selector(response.text)
        categories = sel.xpath('//li[@class="all-categories"]/ul/li/a/@href').getall()
        category_urls = [BASE_URL + url  for url in categories]

        for url in category_urls:
                category_item = CategoryItem(url=url)
                category_item.save()
                self.scrape_category_pages(url)

    def scrape_category_pages(self, category_url):
        parsed = urlparse(category_url)
        category_path = parsed.path.strip("/") 
        base_category_url = f"{BASE_URL}/{category_path}"

        page_number = 1
        while True:
                if page_number == 1:
                    paged_url = base_category_url
                else:
                    paged_url = f"{base_category_url}?pagenumber={page_number}"     

                response = requests.get(paged_url, headers=HEADERS)

                if response.status_code == 200:
                    sel = Selector(response.text)
                    product_urls = sel.xpath('//h2[@class="product-title"]/a/@href').getall()

                    if not product_urls:
                        break

                    self.scrape_pdp_links(sel)
                    page_number += 1

                else:
                    if response.status_code == 500:
                         break
                    else:
                        failed_item = FailedItem(url=category_url, source="crawler")
                        failed_item.save()
                        page_number += 1

    def scrape_pdp_links(self, selector):
        product_urls = selector.xpath('//h2[@class="product-title"]/a/@href').getall()

        for url in product_urls:
            pdp_url = {"url":f"https://www.almayaonline.com{url}"}
            logging.info(pdp_url)
            data_item = ProductUrlItem(**pdp_url)
            data_item.save()
            

if __name__ == "__main__":
    crawler = Crawler()
    crawler.start()