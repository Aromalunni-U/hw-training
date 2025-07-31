from curl_cffi import requests
from parsel import Selector
import json

HEADERS = {
    "Pragma": "no-cache",
    "Priority": "u=0, i",
    "Sec-CH-UA": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": '"Linux"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}


################## CRAWLER ####################

page_no = 1
category_url = "https://www.netto-online.de/gartenmoebel/c-N0500"

while True:

    url = category_url if page_no == 1 else f"{category_url}/{page_no}"

    response = requests.get(url=url, headers=HEADERS , impersonate="chrome")
    if response.status_code == 200:
        sel = Selector(response.text)

        pdp_urls = sel.xpath('//div[@class="product clearfix"]/a/@href').getall()

        if not pdp_urls:
            break

        for url in pdp_urls:
            print(url)
        
        page_no +=1

################ PARSER ######################
        
url = "https://www.netto-online.de/vitalmaxx-kniebandage-mit-kupferfasern/p-1847437000"

response = requests.get(url=url, headers=HEADERS, impersonate="chrome")

sel = Selector(response.text)

PROMO_DESCRIPTION_XPATH = '//span[contains(@class, "tc-product-pricesaving")]/text()'
PRICE_XPATH = 'string(//span[span[@class="product__current-price--digits-after-comma"]])'
INSTOCK_XPATH = '//span[contains(@class, "product-availability__text")]/text()'
PRODUCT_DESCRIPTION_XPATH = '//div[contains(@class, "tc-product-description")]//p/text()'

promotion_description = sel.xpath(PROMO_DESCRIPTION_XPATH).get()
price_was = sel.xpath(PRICE_XPATH).get()
instock = sel.xpath(INSTOCK_XPATH).get()
breadcrumb = sel.xpath('//ol[contains(@class, "breadcrumb")]//span[@itemprop="name"]/text()').getall()
product_description = sel.xpath(PROMO_DESCRIPTION_XPATH).getall()

json_ld = sel.xpath('//script[@type="application/ld+json"]/text()').get()
json_ld = json_ld.replace('\n', '').replace('\r', '').strip()
data = json.loads(json_ld)

offers = data.get("offers", {})
aggregate_rating = data.get("aggregateRating", {})

product_name = data.get("name", "")
brand = data.get("brand",{}).get("name", "")
selling_price = offers.get("price", "")
currency = offers.get("priceCurrency", "")
rating = aggregate_rating.get("ratingValue", "")
review = aggregate_rating.get("reviewCount", "")
image = data.get("image", "")

instock = True if instock and instock.lower().strip() == "auf lager" else False
product_description = " ".join(product_description) if product_description else ""
breadcrumb = " > ".join(breadcrumb)

