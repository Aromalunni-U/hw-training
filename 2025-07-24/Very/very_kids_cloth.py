import re
import json
import requests
import logging
from parsel import Selector
from pymongo import MongoClient
from settings import (
    HEADERS, category_url, MONGO_URI, DB_NAME, DATA_COLLECTION
)


class Crawler:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.collection = self.client[DB_NAME][DATA_COLLECTION]
    
    def start(self):

        page_no = 1
        count = 1

        while True:
            url = category_url if page_no == 1 else f"{category_url}?page={page_no}"

            if count > 200:
                break 

            response = requests.get(url=url, headers=HEADERS)
            if response.status_code == 200:

                sel = Selector(response.text)

                pdp_urls = sel.xpath('//a[@data-testid="fuse-complex-product-card__link"]/@href').getall()
                pdp_urls = [f"https://www.very.co.uk{url}" for url in pdp_urls]

                if not pdp_urls:
                    break

                for link in pdp_urls:
                    response = requests.get(url = link, headers= HEADERS) 

                    if response.status_code == 200:
                        self.parse_item(response, link)
                        count += 1
                    else:
                        logging.error(f"Status code: {response.status_code}")

                page_no += 1

            else:
                logging.error(f"Status code: {response.status_code}")
                break

    def parse_item(self, response, link):

        sel = Selector(response.text)

        PRODUCT_NAME  = '//span[@data-testid="product_title"]/text()'
        BRAND_XPATH = '//span[@data-testid="product_brand"]/text()'
        REGULAR_PRICE_XPATH = '//p[@data-testid="product_price_previous" or @data-testid="product_price_previousFrom"]/text()'
        REVIEW_XPATH = '//a[@data-testid="rating-and-reviews-summary_rating__review"]/text()'
        RATING_XPATH = '//span[contains(text(), "out of 5 stars")]/text()'
        IMAGE_XPATH = '//picture/img/@src'
        PRODUCT_DESCRIPTION_XPATH = '//strong[contains(text(), "Details") or contains(text(), "Reasons to love")]/following-sibling::ul/li/text()'
        SIZE_XPATH = '//label[contains(@for, "size") or contains(@for, "years")]/span/text()'
        MATERIAL_CARE_XPATH = '//strong[contains(text(), "Material & Care")]/following-sibling::ul/li/text()'
        JSON_DATA_XPATH = '//script[@type="application/ld+json"]/text()'
        PROMO_XPARTH = '//p[contains(@data-testid, "product_price_current")]/text()'


        try:
            json_data = sel.xpath(JSON_DATA_XPATH).get()
            data = json.loads(json_data)

            offers = data.get("offers", [])
            if offers:
                first_offer = offers[0]
                selling_price = first_offer.get("price")
                availability = first_offer.get("availability")
                currency = first_offer.get("priceCurrency")
            else:
                selling_price, availability, currency = "", "", ""

            product_name =  sel.xpath(PRODUCT_NAME).get()
            brand = sel.xpath(BRAND_XPATH).get()
            regular_price = sel.xpath(REGULAR_PRICE_XPATH).get()
            review = sel.xpath(REVIEW_XPATH).get()
            rating = sel.xpath(RATING_XPATH).get()
            image = sel.xpath(IMAGE_XPATH).get()
            product_description = sel.xpath(PRODUCT_DESCRIPTION_XPATH).getall()
            size = sel.xpath(SIZE_XPATH).getall()
            material_care = sel.xpath(MATERIAL_CARE_XPATH).getall()
            promotion_description_data = sel.xpath(PROMO_XPARTH).get()

            product_id = link.split("/")[-1].replace(".prd", "")
            regular_price = regular_price.replace("From ", "").replace("Â£", "") if regular_price else ""
            promotion_description =  re.search(r'\((.*?)\)', promotion_description_data)
            promotion_description = promotion_description.group(1) if promotion_description else ""
            promotion_description = promotion_description if "From" not in promotion_description else ""

            product_description = ", ".join(product_description).split(", Material Content")[0] if product_description else ""
            material_care = material_care if material_care else ""
            review = review.replace(" reviews", "") if review else ""
            rating = rating.replace(" out of 5 stars", "") if rating else ""
            availability = True if availability == "InStock" else False

            item = {}

            item["pdp_url"] = link
            item["product_id"] = product_id
            item["product_name"] = product_name
            item["brand"] = brand
            item["currency"] = currency
            item["selling_price"] = selling_price
            item["regular_price"] = regular_price
            item["promotion_description"] = promotion_description
            item["review"] = review
            item["rating"] = rating
            item["image"] = image
            item["product_description"] = product_description
            item["size"] = size
            item["material_care"] = material_care
            item["availability"] = availability

            logging.info(item)
            self.collection.insert_one(item)
            
        except Exception as e:
            logging.error(f"Error : {e}")



if __name__ == "__main__":
    crawler = Crawler()
    crawler.start()
