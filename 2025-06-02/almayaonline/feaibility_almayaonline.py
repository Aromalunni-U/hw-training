import requests
from parsel import Selector

url = "https://www.almayaonline.com/fresh-fruits-and-vegetables"

headers = {
    "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

######################## CRAWLER ##########################

response = requests.get(url,headers=headers)
sel = Selector(response.text)

pdp_url = sel.xpath('//h2[@class="product-title"]/a/@href').getall()

######################## PARSER ###########################

url = "https://www.almayaonline.com/black-grapes-1pc"

response = requests.get(url,headers=headers)
sel = Selector(response.text)

product_name_xpath = '//div[@class="product-name"]/h1/text()'
unique_id_xpath = '//div[@data-productid]/@data-productid'
price_xpath = '//div[@class="product-price"]/span/text()'
images_xpath = '//div[@class="picture"]/img/@src'
description_xpath = '//div[@class="full-description"]/text()'

product_name = sel.xpath(product_name_xpath).get()
unique_id = sel.xpath(unique_id_xpath).get()
price = sel.xpath(price_xpath).get()
image = sel.xpath(images_xpath).get()
product_description = sel.xpath(description_xpath).get()

currency, regular_price = price.strip().split(" ")

