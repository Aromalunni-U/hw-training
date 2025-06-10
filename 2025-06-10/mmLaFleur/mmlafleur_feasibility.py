import requests
from parsel import Selector
import re

HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "accept-language":"en-US,en;q=0.9,hi;q=0.8",
    'Connection': 'keep-alive',
    "referer":"https://mmlafleur.com/"
}


############################# CRAWLER ##################################

url = "https://mmlafleur.com/collections/dresses"

response = requests.get(url,headers=HEADERS)

sel = Selector(response.text)
script_text = sel.xpath("//script[@id='web-pixels-manager-setup']/text()").get()

product_urls = re.findall(r'"url":"(/products/[^"]+)"', script_text)
pdp_urls = ["https://mmlafleur.com" + path for path in product_urls]


########################### PARSER ###################################


pdp_url = "https://mmlafleur.com/products/paige-compact-cotton-top-black"


response = requests.get(pdp_url,headers=HEADERS)
sel = Selector(response.text)

product_name_xpath = "//h1[contains(@class,'ProductMeta__Title')]/text()"
price_xpath = "//span[@class='ProductMeta__Price Price']/text()"
sales_price_xpath = '//span[@class="ProductMeta__Price Price Price--highlight"]/text()'
original_price_xpath = '//span[@class="ProductMeta__Price Price Price--compareAt"]/text()'
script_text_xpath = '//script[contains(., "wishlist.currentProductMeta")]/text()'

product_name = sel.xpath(product_name_xpath).get()
price = sel.xpath(price_xpath).get()
script_text = sel.xpath(script_text_xpath).get()

if price:
    original_price = price
    sales_price = 0
else:
    original_price = sel.xpath(original_price_xpath).get()
    sales_price = sel.xpath(sales_price_xpath).get()

sku = re.search(r"sku:\s*'([^']+)'", script_text)
category = re.search(r"category:\s*'([^']+)'", script_text)
brand = re.search(r"brand:\s*'([^']+)'", script_text)
empi = re.search(r"empi:\s*'([^']+)'", script_text)

url = "https://api-cdn.yotpo.com/v3/storefront/store/hnkji0K4D1gfLABJN4GggiPDnm5GQdw5TAk6pRSp/product/{}/reviews".format(empi.group(1))

params = {
    "page": 1,
    "perPage": 50,
    "sort": "date,rating,badge,images"
}
response = requests.get(url, params=params)
data = response.json()

total_number_of_reviews = data.get("bottomline",{}).get("totalReview","")
stars = data.get("bottomline",{}).get("starDistribution",{})

if stars:
    star_1 = stars.get("1",0)
    star_2 = stars.get("2",0)
    star_3 = stars.get("3",0)
    star_4 = stars.get("4",0)
    star_5 = stars.get("5",0)

if total_number_of_reviews > 50:
    review_text = []
    total_pages = (total_number_of_reviews // 50) + (1 if total_number_of_reviews % 50 > 0 else 0)
    print(total_pages)
    for page in range(1, total_pages + 1):
        params["page"] = page
        response = requests.get(url, params=params)
        reviews = response.json().get("reviews", [])
        review_list = [review.get("content", "") for review in reviews if review.get("content")]
        review_text.extend(review_list)
else:
    raw_reviews = data.get("reviews",[])
    review_text = [review.get("content","") for review in raw_reviews]


