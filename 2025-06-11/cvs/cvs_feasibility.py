from curl_cffi import requests
from parsel import Selector
import re
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "TE": "trailers"
}

################################ CRAWLER ##################################

url = "https://www.cvs.com/shop/vitamins/supplements"

response = requests.get(
    url,
    headers=HEADERS,
    timeout=20,
)

if response.status_code == 200:
    sel = Selector(response.text)
    script_txt = sel.xpath('//script[@id="schema-json-ld"]/text()').get()
    urls = re.findall(r'"url"\s*:\s*"([^"]+)"', script_txt)
    print(urls)
    print(len(urls))
else:
    print(response.status_code)

############################## PARSER ######################################


pdp_url = "https://www.cvs.com/shop/preservision-areds-2-formula-eye-vitamin-mineral-supplement-soft-gels-prodid-1040130"

response =  requests.get(url = pdp_url,
                        headers=HEADERS,
                        timeout=20,)

if response.status_code == 200:
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

    
    ingredients = ingredients_match.group(1) if ingredients_match else ""
    warnings = warnings_match.group(1) if warnings_match else ""
    feeding_recommendation = feed_match.group(1) if feed_match else ""
    promotion_description =  promo.group(1) if promo else ""
    unit_price =  unit_price.group(1) if unit_price else ""

