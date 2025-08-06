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
pdp_url = "https://www.knuspr.de/en-DE/6509-alnatura-organic-chickpea-flour"

response = requests.get(pdp_url, headers=HEADERS)
if response.status_code == 200:
    sel = Selector(response.text)

    PRODUCT_NAME_XPATH = '//h1/a/text()'
    BRAND_XPATH = '//h1/a/p/text()'
    SELLING_PRICE_XPATH = '//span[@data-test="product-price"]/text()'
    GRAMMAGE_XPATH = '//span[@class="detailQuantity"]/text()'
    PRODUCT_DESC_XPATH = '''
        //div[@class="ckContent"]/div[not(@class="autoTranslationAnnouncement")]//p//text() |
        //div[@class="ckContent"]/div[not(@class="autoTranslationAnnouncement")]//text()
    '''
    IMAGE_XPATH = '//div[contains(@class, "sc-c31413-1")]//img/@src'
    COUNTRY_XPATH = '//span[@class="categoryName"]/text()'
    BREADCRUMB_XPATH = '//ul[@data-test="pnlBreadcrumbs"]/li/a/text()'
    NUTRITIONS_XPATH = '//div[h2[contains(text(),"Nutritional")]]//tr'
    ALLERGENCE_XPATH = '//div[h2[contains(text(),"Allergens")]]//tr//text()'


    product_name = sel.xpath(PRODUCT_NAME_XPATH).get()
    brand = sel.xpath(BRAND_XPATH).get()
    selling_price = sel.xpath(SELLING_PRICE_XPATH).get()
    grammage= sel.xpath(GRAMMAGE_XPATH).get()
    product_description = sel.xpath(PRODUCT_DESC_XPATH).getall()
    image = sel.xpath(IMAGE_XPATH).get()   
    country_of_orgin = sel.xpath(COUNTRY_XPATH).get()
    breadcrumb = sel.xpath(BREADCRUMB_XPATH).getall()   
    allergens = sel.xpath(ALLERGENCE_XPATH).getall()


    product_id = pdp_url.split("/")[-1].split("-")[0]
    brand = brand.strip() if brand else ""
    selling_price = selling_price.replace("€", "").strip() if selling_price else ""

    if grammage:
        grammage_quantity = grammage.split()[0]
        grammage_unit = grammage.split()[-1]
    else:
        grammage_quantity, grammage_unit , = "", ""

    product_description = " ".join(product_description) if product_description else ""

    nutritions  = {}
    table_rows = sel.xpath(NUTRITIONS_XPATH)
    for row in table_rows:
        key = row.xpath('./td[1]/text()').get()
        value = row.xpath('./td[2]//text()').getall()
        nutritions[key] = "".join(value).strip()

    allergens = " ".join(allergens) if allergens else ""

        
else:
    logging.error(f"Status code {response.status_code}")


