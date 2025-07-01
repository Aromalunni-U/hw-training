import requests
from parsel import Selector
import logging
from settings import HEADERS



################# CRAWLER ###################
 
page_no = 1

while True:
    next_page_url = f"https://www2.hm.com/en_in/women/shop-by-product/tops.html?productTypes=Top&page={page_no}"
    
    logging.info(f"Page: {page_no} - {next_page_url}")

    response = requests.get(next_page_url, headers= HEADERS)
    if response.status_code != 200:
        logging.error(f"Failed : {response.status_code}")
        break

    sel = Selector(response.text)
    pdp_urls = sel.xpath('//div[@class="e4889e"]/a/@href').getall()

    for url in pdp_urls:
        logging.info(url)

    page_no += 1


################### PARSER ####################

url = "https://www2.hm.com/en_in/productpage.1292587001.html"

response = requests.get(url, headers= HEADERS)
sel = Selector(response.text)

PRODUCT_NAME_XPATH = '//h1[@class="fe9348 bdb3fa d582fb"]/text()'
REGULAR_PRICE_XPATH = '//span[@class="e70f50 d7cab8 d9ca8b"]/text()'
ART_NUMBER_XPATH = '//p[contains(text(), "Art. No.")]/text()'
COMPOSITION_XPATH = '//span[@class="e95b5c f8c1e9 efef57"]/text()'
IMAGE_XPATH = '//ul[@data-testid="grid-gallery"]//img/@src'
CLOTHING_LENGTH = '//dt[contains(text(), "Length")]/following-sibling::dd/text()'
CLOTHING_FIT = '//dt[contains(text(), "Fit")]/following-sibling::dd/text()'
COUNTRY_OF_ORGIN_XPATH = '//dt[contains(text(), "Country of production")]/following-sibling::dd/text()'
NECK_STYLE = '//dt[contains(text(), "Neckline")]/following-sibling::dd/text()'
STYLE_XPATH = '//dt[contains(text(), "Style")]/following-sibling::dd/text()'
CARE_INSTRUCTION = '//h3[contains(text(), "Care instructions")]/following-sibling::ul/li/text()'
SIZE_XPATH = '//dt[contains(text(), "Size")]/following-sibling::dd/text()'
COLOR_XPATH = '//dt[contains(text(), "Description")]/following-sibling::dd/text()'
SLEEVE_LENGTH = '//dt[contains(text(), "Sleeve Length")]/following-sibling::dd/text()'

product_name = sel.xpath(PRODUCT_NAME_XPATH).get()
regular_price = sel.xpath(REGULAR_PRICE_XPATH).get()
art_number = sel.xpath(ART_NUMBER_XPATH).getall()
material_composition = sel.xpath(COMPOSITION_XPATH).get()
images = sel.xpath(IMAGE_XPATH).getall()
clothing_length = sel.xpath(CLOTHING_LENGTH).get()
clothing_fit = sel.xpath(CLOTHING_FIT).get()
country_of_origin = sel.xpath(COUNTRY_OF_ORGIN_XPATH).get()
neck_style = sel.xpath(NECK_STYLE).get()
style = sel.xpath(STYLE_XPATH).get()
care_instruction = sel.xpath(CARE_INSTRUCTION).getall()
size = sel.xpath(SIZE_XPATH).getall()
color  = sel.xpath(COLOR_XPATH).get()
sleeve_length = sel.xpath(SLEEVE_LENGTH).get()

size = [s.split(":")[0] for s in size]
art_number = "".join(art_number).split(":")[-1].strip() if art_number else ""
color = color.split(",")[0] if color else ""


