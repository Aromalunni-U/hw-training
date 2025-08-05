import requests
import logging
from settings import HEADERS, headers
from parsel import Selector

################ CRAWLER ##################

def crawler(product_id):

    params = {
        'products': product_id,
        'categoryType': 'normal',
    }

    api_url = 'https://www.knuspr.de/api/v1/products/card'
    response = requests.get(api_url, params=params, headers=headers)
    if response.status_code == 200:
        products = response.json()

        for product in products:
            product_id = product.get("productId", "")
            pdp_url = product.get("slug", "")

            pdp_url = f"https://www.knuspr.de/en-DE/{product_id}-{pdp_url}"
            logging.info(pdp_url)
    else:
        logging.error(f"Status code {response.status_code}")




category_id = 4742
page = 1
while True:
    url = f"https://www.knuspr.de/api/v1/categories/normal/{category_id}/products"
    params = {
            "page": page,
            "size": 14,
            "sort": "recommended"
        }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()

        product_id = data.get("productIds", [])
        if not product_id:
            break

        crawler(product_id)

        page += 1
    else:
        logging.error(f"Status code {response.status_code}")


    
############### PARSER ####################3

pdp_url = "https://www.knuspr.de/en-DE/25360-bauckhof-bio-waffeln-pfannkuchen-glutenfrei"

response = requests.get(pdp_url, headers=HEADERS)
if response.status_code == 200:
    sel = Selector(response.text)

    product_name = sel.xpath('//h1/a/text()').get()
    brand = sel.xpath('//h1/a/p/text()').get()
    selling_price = sel.xpath('//span[@data-test="product-price"]/text()').get()
    grammage= sel.xpath('//span[@class="detailQuantity"]/text()').get()
    product_description = sel.xpath('//div[@class="ckContent"]/p/text()').getall()
    image = sel.xpath('//div/picture/img/@src').get()   

    product_id = pdp_url.split("/")[-1].split("-")[0]


    brand = brand.strip() if brand else ""
    selling_price = selling_price.replace("€", "").strip() if selling_price else ""

    if grammage:
        grammage_quantity = grammage.split()[0]
        grammage_unit = grammage.split()[-1]
    else:
        grammage_quantity, grammage_unit , = "", ""

    product_description = " ".join(product_description) if product_description else ""

else:
    logging.error(f"Status code {response.status_code}")