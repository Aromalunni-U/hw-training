import requests
from parsel import Selector
import json

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "accept-language":"en-US,en;q=0.9,hi;q=0.8",
    'Connection': 'keep-alive',
}


ean_list = [
    "76344107521", "76344107491", "76344108115", "76344107538", "76344118572",
    "76344105398", "76344107262", "76344108320", "76344116639", "76344106661",
    "64992523206", "64992525200", "64992523602", "64992525118", "64992714369",
    "64992714376", "64992719814", "64992719807", "5060184240512", "5060184240703",
    "5060184240598", "5060184244909", "5060184240109", "5425039485256", "5425039485010",
    "5425039485263", "5425039485034", "5425039485317", "5407009646591", "5407009640353",
    "5407009640391", "5407009640636", "5407009641022", "3182551055672", "3182551055788",
    "3182551055719", "3182551055825", "9003579008362", "3182550704625", "3182550706933",
    "9003579013793", "9003579013861"
]


######################### CRAWLER #######################################

search_url = "https://www.discus.nl/find/?filter%5Ball%5D={}"



for ean in ean_list:
    url = search_url.format(ean)
    response = requests.get(url, headers=headers)
    sel = Selector(response.text)

    if response.status_code == 200:
        pdp_url = sel.xpath('//div[@class="UIHeading element-content"]/a/@href').get()
        if pdp_url:
            print(pdp_url)


########################## PARSER ####################################


pdp_url = 'https://www.discus.nl/product/royal-canin-shn-mini-adult-2-kg/'
 
response = requests.get(pdp_url,headers=headers)
sel = Selector(response.text)

product_name_xpath = '//div[@class="UIHeading element-content"]/h1/text()'
price_was_xpath = '//span[@class="old-price"]/text()'
breadcrumb_xpath = '//ol[@class="breadcrumbs list-unstyled"]/li/a/span/text()'
description_xpath = '//div[@id="63a8aac81a71f461c56df534b554df67"]/div/span/p/text()'
images_xpath = '//div[@class="bx-pager-wrapper"]/div/a/img/@src'
script_xpath = '//script[@id="product-views-ProductView-datalayers"]/text()'

script_content = sel.xpath(script_xpath).get()
product_data = script_content.find("dataLayer.push({", script_content.find("dataLayer.push({") + 1)
product_data = script_content[len("dataLayer.push(") + product_data:].replace(");","").replace("'", '"')
product_data = json.loads(product_data)
item = product_data['ecommerce']['items'][0]

currency = product_data['ecommerce']['currency']
selling_price = item['price']
brand = item['item_brand']

product_name = sel.xpath(product_name_xpath).get()
price_was = sel.xpath(price_was_xpath).get()
breadcrumb = sel.xpath(breadcrumb_xpath).getall()
description = sel.xpath(description_xpath).get()
images = sel.xpath(images_xpath).getall()



