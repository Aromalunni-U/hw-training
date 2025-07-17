import requests
from parsel import Selector
from settings import HEADERS
import re
import json

############## CRAWLER ####################

offset = 0
while True:

    url = f"https://www.lidl.nl/q/query/alle-producten-keuken-&-huishouden?offset={offset}"
    response = requests.get(url, headers = HEADERS)

    sel = Selector(response.text)
    data = sel.xpath('//script[@type="application/json"]/text()').get()

    if data:
        pdp_urls = re.findall(r'\/p\/[a-zA-Z0-9\-/]+', data)
        pdp_urls = [f"https://www.lidl.nl{url}" for url in pdp_urls]

        if not pdp_urls:
            break
    else:
        break

    offset += 48


##################### PARSER ################

url  = "https://www.lidl.nl/p/grillmeister-gas-bbq-3-branders/p100387392"

response = requests.get(url, headers = HEADERS)

sel = Selector(response.text)

PRODUCT_NAME_XPATH = '//h1[@class="heading__title"]/text()'
PRICE_WAS_XPATH = '//div[@class="ods-price__stroke-price"]/s/text()'
PERCENTAGE_DESCOUNT_XPATH = '//span[@class="ods-price__box-content-text-el"]/text()'
SELLING_PRICE_XPATH = '//div[@class="ods-price__value"]/text()'
IMAGES_XPATH = '//img[@class="thumbnail-slide__image"]/@src'
REVIEW_XPATH = '//span[@class="ods-rating__info-total"]/text()'
RATING_XPATH = '//span[@class="ods-rating__info"]/text()'
BREADCRUMB_XPATH = '//span[@class="ods-breadcrumbs__link-title"]/text()'
MATERIAL_XPATH = "//p[strong[contains(text(), 'Materiaal')]]/following-sibling::*[1]//text()"
CARE_INSTRUCTIONS = "//p[strong[contains(text(), 'Onderhoudsinstructies')]]/following-sibling::*[1]//text()"
BRAND_XPATH = '//a[@class="heading__brand"]/text()'
PROPERTIES_XPATH = "//p[strong[contains(text(), 'Eigenschappen')]]/following-sibling::ul/li/text()"
SIZE_XPATH = '//ul[@class="attributes-one__options"]//label[@class="option"]/text()'
SCRIPT_DATA_XPATH = '//script[@id="__NUXT_DATA__"]/text()'
COLOR_XPATH = '//p[strong[contains(text(), "Kleuren")]]/text()[1]'


product_name = sel.xpath(PRODUCT_NAME_XPATH).get()
price_was = sel.xpath(PRICE_WAS_XPATH).get()
percentage_discount = sel.xpath(PERCENTAGE_DESCOUNT_XPATH).get()
selling_price = sel.xpath(SELLING_PRICE_XPATH).get()
images = sel.xpath(IMAGES_XPATH).getall()
review = sel.xpath(REVIEW_XPATH).get()
rating = sel.xpath(RATING_XPATH).get()
breadcrumb = sel.xpath(BREADCRUMB_XPATH).getall()
brand = sel.xpath(BRAND_XPATH).get()
size = sel.xpath(SIZE_XPATH).getall()
script_data = sel.xpath(SCRIPT_DATA_XPATH).get()


data = json.loads(script_data)
flat = json.dumps(data)
decoded_data = flat.encode().decode('unicode_escape')  

sel = Selector(text=decoded_data)

color = sel.xpath().get()
material = sel.xpath(MATERIAL_XPATH).getall()
care_instructions = sel.xpath(CARE_INSTRUCTIONS).getall()
properties = sel.xpath(PROPERTIES_XPATH).getall()

features = {}
for row in sel.xpath('//table//tr'):
    key = row.xpath('./td[1]//strong/text()').get()
    value = row.xpath('./td[2]//text()').get()
    if key and value:
        features[key.strip().rstrip(':')] = value.strip()

