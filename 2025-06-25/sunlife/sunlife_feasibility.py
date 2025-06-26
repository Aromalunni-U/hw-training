import requests
from parsel import Selector

BASE_URL = "https://sunlife.qa/"

url = "https://sunlife.qa/ajax/categoriesdropdown"

api_url = "https://nm61sop7f5thlwecp.a1.typesense.net/multi_search?x-typesense-api-key=tSKaWnwrBRsMZnIGKLFCxNDM3qS7ChXz"

HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "accept-language":"en-US,en;q=0.9,hi;q=0.8",
    'Connection': 'keep-alive',
}


################### CATEGORY  ##########################

response = requests.get(url=url, headers= HEADERS)
sel = Selector(response.text)
catefory_url = sel.xpath('//a[@class="catname smaller"]/@href').getall()


################## SUB CATEGORY #########################

for url in catefory_url:
    response = requests.get(url=url, headers= HEADERS)
    sel = Selector(response.text)
    sub_category = sel.xpath('//p[@class="heading-card pb-30"]/a/@href').getall()

################## CRAWLER ##############################


url = "https://sunlife.qa/product-category/coloring"

page_no = 1
category_name = url.split("/")[-1]

while True:
    payload = f'''
        {{
          "searches": [
            {{
              "query_by": "name,sku",
              "sort_by": "is_out_stock:asc,in_promo:desc,name:asc",
              "highlight_full_fields": "name,sku",
              "collection": "ec_products",
              "q": "*",
              "facet_by": "brand,categories,offer_label_en,price",
              "filter_by": "categories:=[{category_name}]",
              "max_facet_values": 50,
              "page": {page_no}
            }}
          ]
        }}
        '''    
    response = requests.post(url=api_url, data=payload, headers=HEADERS)
    data = response.json()
 

    products = data.get("results",[])[0].get("hits",[])
    if not products:
        break

    for product in products:
        pdp_url = product.get("document",{}).get("url","")
        print(pdp_url)

    page_no +=1


########################### PARSER ###############################

url = "https://sunlife.qa/shop/placentor-vegetal-anti-age-plumping-lip-balm-4gm"

response = requests.get(url=url, headers= HEADERS)

sel = Selector(response.text)

PRODUCT_NAME_XPATH = '//h1[@class="title-detail text-capitalize"]/text()'
INSTOCK_XPATH = '//span[@class="number-items-available"]/span/text()'
DISCOUNT_XPATH = '//span[@class="percentage-off"]/text()'
SALE_PRICE_XPATH = '//span[@class="current-price text-brand"]/text()'
MRP_XPATH = '//span[@class="old-price font-md ml-15 "]/text()'

product_name = sel.xpath(PRODUCT_NAME_XPATH).getall()
instock = sel.xpath(INSTOCK_XPATH).get()
discount = sel.xpath(DISCOUNT_XPATH).get()
sale_price = sel.xpath(SALE_PRICE_XPATH).get()
mrp = sel.xpath(MRP_XPATH).get()

product_name = ' '.join([text.strip() for text in product_name if text.strip()])
instock = True if instock.lower().strip() == "in stock" else False

