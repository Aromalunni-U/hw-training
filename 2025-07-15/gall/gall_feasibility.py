import requests
import logging
from parsel import Selector
from settings import HEADERS, BASE_URL



############# CRAWLER ############

url  = "https://www.gall.nl/mixen/gin/"

while True:

    res = requests.get(url, headers= HEADERS)
    sel = Selector(res.text)

    if res.status_code == 200:

        pdp_urls = sel.xpath('//a[@class="ptile_link"]/@href').getall()
        pdp_urls = [f"{BASE_URL}{url}" for url in pdp_urls]

        next_page = sel.xpath("//a[@aria-label='volgende pagina']/@href").get()

        if not next_page:
            break

        url = f"https://www.gall.nl{next_page}"
        
    else:
        logging.info(f'Status code : {res.status_code}')
        break


############### PARSER ################

url = "https://www.gall.nl/martini-floreale-75cl-149276.html"

res = requests.get(url, headers= HEADERS)
sel = Selector(res.text)

PRODUCT_NAME_XPATH = "//h1[@class='pdp-info_name']/text()"
REGULAR_PRICE_XPATH = 'concat(//span[@class="price-value "]/text(), //span[@class="price-value "]/@data-decimals)'
PRODUCT_DESCRIPTION = "//div[@id='product-description']/p/text()"
BREADCRUMB_XPATH = "//a[@class='breadcrumb__label is--link']/span/text()"
RATING_XPATH = "//span[@class='rating_label']/text()"
REVIEW_XPATH = "//span[@class='rating_label']/@data-count"
IMAGE_XPATH = "//figure[@class='a-image image-contain pdp-info_image']/img/@src"
ALCHOLE_PER_XPATH = "//td[text()='Alcoholpercentage']/following-sibling::td/text()"
INGREDIENT_XPATH = "//td[text()='Ingrediënten']/following-sibling::td/text()"
ALLERGENS_XPATH = "//td[text()='Allergie-informatie']/following-sibling::td/text()"
ALCHOLE_VOL_XPATH = "//td[text()='Inhoud']/following-sibling::td/text()"
INSTOCK_XPATH = '//div[contains(@class, "product-online-availability")]/text()'
NUTRITIONS_XPATH = '//div[@class="product-nutritional-values"]//tr[not(@class="product-nutritional-serving")]'

product_name = sel.xpath(PRODUCT_NAME_XPATH).get()
regular_price = sel.xpath(REGULAR_PRICE_XPATH).get()
product_description = sel.xpath(PRODUCT_DESCRIPTION).get()
breadcrumb = sel.xpath(BREADCRUMB_XPATH).getall()
rating = sel.xpath(RATING_XPATH).get()
review = sel.xpath(REVIEW_XPATH).get()
image = sel.xpath(IMAGE_XPATH).get()
alchole_percentage = sel.xpath(ALCHOLE_PER_XPATH).get()
ingredient = sel.xpath(INGREDIENT_XPATH).get()
allergens = sel.xpath(ALLERGENS_XPATH).get()
alchol_by_volume = sel.xpath(ALCHOLE_VOL_XPATH).get()
instock = sel.xpath(INSTOCK_XPATH).get()

instock = True if instock == "Online op voorraad" else False

nutritions  = {}
table_rows = sel.xpath(NUTRITIONS_XPATH)
for row in table_rows:
    key = row.xpath('./td[1]/text()').get()
    value = row.xpath('./td[2]/text()').get()
    nutritions[key] = value

