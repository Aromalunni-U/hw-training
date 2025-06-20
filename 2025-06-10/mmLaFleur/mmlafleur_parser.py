import re
import requests
from pymongo import MongoClient
import logging
from settings import MONGO_URI, DB_NAME, CRAWLER_COLLECTION, HEADERS
from parsel import Selector
from mongoengine import connect
from mmlafleur_items import ProductItem, FailedItem


class Parser:
    def __init__(self):
        connect(DB_NAME, host=MONGO_URI, alias="default")
        self.client = MongoClient(MONGO_URI)
        self.crawler_collection = self.client[DB_NAME][CRAWLER_COLLECTION]

    def start(self):
        links = self.crawler_collection.find()
        for link in links:
            link = link.get("url")
            response = requests.get(link,headers=HEADERS)
            if response.status_code == 200:
                self.parse_iem(link,response)
            else:
                product_item = FailedItem(url = link, source ="parser")
                product_item.save()

    def parse_iem(self,url,response):
        sel = Selector(response.text)

        product_name_xpath = "//h1[contains(@class,'ProductMeta__Title')]/text()"
        price_xpath = "//span[@class='ProductMeta__Price Price']/text()"
        sales_price_xpath = '//span[@class="ProductMeta__Price Price Price--highlight"]/text()'
        original_price_xpath = '//span[@class="ProductMeta__Price Price Price--compareAt"]/text()'
        script_text_xpath = '//script[contains(., "wishlist.currentProductMeta")]/text()'

        product_name = sel.xpath(product_name_xpath).get()
        price = sel.xpath(price_xpath).get()
        script_text = sel.xpath(script_text_xpath).get()

        product_sku = re.search(r"sku:\s*'([^']+)'", script_text)
        category = re.search(r"category:\s*'([^']+)'", script_text)
        brand = re.search(r"brand:\s*'([^']+)'", script_text)
        empi = re.search(r"empi:\s*'([^']+)'", script_text)

        if price:
            original_price = price
            sales_price = 0
        else:
            original_price = sel.xpath(original_price_xpath).get()
            sales_price = sel.xpath(sales_price_xpath).get().replace("$","")

        product_name = product_name.replace("\n","").strip()
        product_sku = product_sku.group(1) if product_sku else ""
        category = category.group(1) if category else ""
        brand = brand.group(1) if brand else ""
        original_price = original_price.replace("$",'')

        page_no = 1
        review_text = []

        while True:
            api_url = "https://api-cdn.yotpo.com/v3/storefront/store/hnkji0K4D1gfLABJN4GggiPDnm5GQdw5TAk6pRSp/product/{}/reviews".format(empi.group(1))

            params = {
                "page": page_no,
                "perPage": 50,
                "sort": "date,rating,badge,images"
            }
            response = requests.get(api_url, params=params)
            data = response.json()

            total_number_of_reviews = data.get("bottomline",{}).get("totalReview",0)
            raw_reviews = data.get("reviews",[])

            stars = data.get("bottomline",{}).get("starDistribution",{})
            if stars:
                star_1 = stars.get("1",0)
                star_2 = stars.get("2",0)
                star_3 = stars.get("3",0)
                star_4 = stars.get("4",0)
                star_5 = stars.get("5",0)
            else:
                star_1, star_2, star_3, star_4, star_5 = 0, 0, 0, 0, 0 
    
            if total_number_of_reviews == 0:
                logging.info(f"No reviews found for: {product_name}")
                return     

            if not raw_reviews:
                break

            review_text.extend([
                                review.get("content", "").replace("\n", "") 
                                for review in raw_reviews
                            ])
            page_no +=1
            
        item = {}

        item["pdp_url"] = url
        item["product_name"] = product_name
        item["product_sku"] = product_sku
        item["original_price"] = original_price
        item["sales_price"] = sales_price
        item["category"] = category
        item["brand"] = brand
        item["total_number_of_reviews"] = total_number_of_reviews
        item["1_star"] = star_1
        item["2_star"] = star_2
        item["3_star"] = star_3
        item["4_star"] = star_4
        item["5_star"] = star_5
        item["review_text"] = review_text

        logging.info(item)
        product_item = ProductItem(**item)
        product_item.save()


if __name__ == "__main__":
    parser_obj = Parser()
    parser_obj.start()