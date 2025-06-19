import logging
import re
import json
from parsel import Selector
from curl_cffi import requests
from settings import HEADERS, DB_NAME, MONGO_URI
from mongoengine import connect
from cvs_items import FailedItem, ProductItem


class Parser:
    def __init__(self,urls):
        connect(DB_NAME, host=MONGO_URI, alias="default")

    def start(self):
        for link in pdp_urls:
            response = requests.get(link,headers=HEADERS)
            if response.status_code == 200:
                self.parse_iem(link,response)
            else:
                failed_url = FailedItem(url=link)
                failed_url.save()

    def parse_iem(self,url,response):
        sel = Selector(response.text)

        product_name_xpath = "//h1/text()"
        rating_xpath  = '//p[contains(@class,"text-xl")]/text()'
        review_xpath = '//p[contains(text(), "reviews")]/text()'
        breadcrumb_xpath = '//nav[@aria-label="breadcrumbs"]//li//span[not(@class="ps-link-leading")]/text()'
        images_xpath = '//div[@role="tablist"]/button/img/@src'

        product_name = sel.xpath(product_name_xpath).get()
        rating = sel.xpath(rating_xpath).get()
        review = sel.xpath(review_xpath).get()
        breadcrumb = sel.xpath(breadcrumb_xpath).getall()
        images = sel.xpath(images_xpath).getall()


        json_ld_text = sel.xpath('//script[@id="schema-json-ld"]/text()').get()
        script_content = sel.xpath(
            '//script[contains(text(), "vendorIngredientsParagraph")]/text()').get()
        script_price_content = sel.xpath(
            '//script[contains(text(), "unitPrice")]/text()').get()
        
                
        product_data = json.loads(json_ld_text)  
        product = product_data[0]

        price = product.get('offers', {}).get('price')
        currency = product.get('offers',{}).get('priceCurrency')
        category = product.get('category', {}).get('@type')  
        product_id = product.get('productID')               
        brand_name = product.get('brand', {}).get('name')

        ingredients_match = re.search(
            r'\\"vendorIngredientsParagraph\\":\\"([^"]+)\\"', script_content)
        warnings_match = re.search(
            r'\\"vendorWarningsParagraph\\":\\"([^"]+)\\"', script_content)
        feed_match = re.search(
            r'\\"vendorDirectionsParagraph\\":\\"([^"]+)\\"', script_content)
        promo = re.search(
            r'\\"promoDescription\\":\\"([^"]+)\\"', script_price_content)
        unit_price = re.search(
            r'\\"unitPrice\\":\\"([^"]+)\\"', script_price_content)
        price_was = re.search(
            r'\\"listPrice\\":\\"([^"]+)\\"', script_price_content)
        product_description = re.search(
            r'\\"vendorDetailsParagraph\\":\\"([^"]+)\\"',response.text)        
        spec_match = re.search(
            r'\\"dynamicAttributes\\":\s*(\{.*?\})', response.text)
        

        category = category.strip() if category else ""
        review = re.search("[0-9]+",review).group() if review else ""
        breadcrumb = " > ".join(breadcrumb)
        ingredients = ingredients_match.group(1) if ingredients_match else ""
        warnings = warnings_match.group(1) if warnings_match else ""
        feeding_recommendation = feed_match.group(1) if feed_match else ""
        promotion_description =  promo.group(1) if promo else ""
        unit_price =  unit_price.group(1) if unit_price else ""
        price_was = price_was.group(1) if price_was else ""
        product_description = product_description.group(1) if product_description else ""

        specification = ""
        if spec_match:
            raw_spec = spec_match.group(1)
            specification = raw_spec.replace('\\"', '"')
            specification = specification.replace('["', '"').replace('"]', '"')

        images = [f"https://www.cvs.com/{img}" for img in images]

        item = {}

        item["pdp_url"] = url
        item["product_name"] = product_name
        item["original_price"] = price
        item["selling_price"] = price_was
        item["currency"] = currency
        item["category"] = category
        item["unique_id"] = product_id 
        item["breadcrumb"] = breadcrumb
        item["brand"] = brand_name
        item["rating"] = rating
        item["review"] = review
        item["unit_price"] = unit_price
        item["ingredients"] = ingredients
        item["warnings"] = warnings
        item["feeding_recommendation"] = feeding_recommendation
        item["promotion_description"] = promotion_description
        item["product_description"] = product_description
        item["product_specifications"] = specification
        item["images"] = images

        logging.info(item)
        data_item = ProductItem(**item)
        data_item.save()


pdp_urls = [
    "https://www.cvs.com/shop/crest-premium-plus-scope-dual-blast-toothpaste-intense-mint-7-2-oz-prodid-637529",
    "https://www.cvs.com/shop/dr-emil-5-htp-plus-brain-mood-sleep-support-capsules-60-ct-prodid-724953",
    "https://www.cvs.com/shop/preservision-areds-2-formula-eye-vitamin-mineral-supplement-soft-gels-prodid-1040130",
    "https://www.cvs.com/shop/nature-s-truth-apple-cider-vinegar-1200-mg-prodid-524868",
    "https://www.cvs.com/shop/olly-probiotic-gummy-tropical-mango-80-ct-prodid-547007",
    "https://www.cvs.com/shop/cvs-health-melatonin-tablets-60-ct-prodid-346979",
    "https://www.cvs.com/shop/ocuvite-eye-vitamin-mineral-supplement-adult-prodid-1040133",
]


if __name__ == "__main__":
    parser = Parser(pdp_urls)
    parser.start()
