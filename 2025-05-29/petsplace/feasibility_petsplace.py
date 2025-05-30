import requests
from parsel import Selector
import re


headers = {
    "accept-encoding":"gzip, deflate, br, zstd",
    "accept-language":"en-US,en;q=0.9,hi;q=0.8",
    'Connection': 'keep-alive',
    "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}


###################### CRAWLER #########################

url = "https://www.petsplace.nl/kat/kattenvoer/kattenbrokken"

response = requests.get(url,headers=headers)

response = Selector(text=response.text)

product_urls = response.xpath(
    '//a[@class="product photo product-item-photo"]/@href').geall()


###################### PARSER ###########################

url = "https://www.petsplace.nl/pro-plan-cat-sterilised-kattenvoer-m-7613036519991-pps"

response = requests.get(url,headers=headers)

response = Selector(response.text)

price_xpath = "//span[@class='price']/text()"
breadcrumb_xpath = "//ul[@class='items']//li//span[@itemprop='name']/text()"
brand_xpath = '//td[@data-td="Merk"]/text()'
packaging_xpath = '//td[@data-td="Verpakking"]/text()'
recommendation_xpath = '//td[@data-td="Aanbeveling"]/text()'
availability_xpath = '//td[@data-td="Beschikbaarheid"]/text()'
weight_xpath = '//td[@data-td="Gewicht"]/text()'
variants_xpath = '//div[@class="configurable-option"]//span[@class="swatch-name"]/text()'
product_description_xpath = "//div[@class='value']/p[position()=1]"
image_xpath = '//img[@class="gallery-placeholder__image"]/@src'
compound_xpath = '//td[@data-td="Samenstelling"]/text()'
ean_xpath = '//td[@data-td="EAN"]/text()'
art_number_xpath = '//td[@data-td="Art.nr."]/text()'
analysis_xpath = '//td[@data-td="Analyse"]/text()'
product_group_xpath = '//td[@data-td="Productgroep"]/text()'
review_xpath = '//a[@class="action view"]/span/text()'
rating_xpath = '//span[@class="grade"]/text()'

price = response.xpath(price_xpath).get()
breadcrumb = response.xpath(breadcrumb_xpath).getall()
brand = response.xpath(brand_xpath).get()
packaging = response.xpath(packaging_xpath).get()
recommendation = response.xpath(recommendation_xpath).get()
availability = response.xpath(availability_xpath).get()
weight = response.xpath(weight_xpath).get() 
variants = response.xpath(variants_xpath).getall()
product_description = response.xpath(product_description_xpath).get()
images = response.xpath(image_xpath).getall()
compount = response.xpath(compound_xpath).get()
ean = response.xpath(ean_xpath).get()
art_number = response.xpath(art_number_xpath).get()
analysis = response.xpath(analysis_xpath).get()
product_group = response.xpath(product_group_xpath).get()
review = response.xpath(review_xpath).get()
rating = response.xpath(rating_xpath).get()

if product_description:
    product_description = re.sub(r'<.*?>', '', product_description)

variants = variants if variants else ""


############## FINDING ######################

# Unique EAN found at the end of each URL