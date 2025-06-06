import requests
from parsel import Selector

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

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "accept-language":"en-US,en;q=0.9,hi;q=0.8",
    'Connection': 'keep-alive',
}

############################ CRAWLER ####################################

search_url = "https://www.dollardog.dk/catalogsearch/result/?q={}"

EAN = '5407009646591'

response = requests.get(search_url.format(EAN),headers=headers)

sel = Selector(response.text)

pdp_url = sel.xpath(
    '//a[@class="product-item-link"]/@href'
).get()


############################ PARSER ###########################

pdp_url = "https://www.dollardog.dk/50-g-top-dog-large-bite-kylling-ec"

response = requests.get(pdp_url,headers=headers)
sel = Selector(response.text)


product_name_xpath = '//span[@class="base"]/text()'
price_xpath = '//span[@class="price"]/text()'
composition_xpath = '//div[@class="data item content"]/p/text()'
description_xpath = '//div[@id="description"]//div[@class="value"]/*[not(self::style)]//text()'
code_xpath = '//div[@class="product attribute sku"]/div/text()'
features_xpath = '//td[@data-th="Specifikationer"]/ul/li/text()'
image_xpath = '//img[@class="gallery-placeholder__image"]/@src'

product_name = sel.xpath(product_name_xpath).get()
price = sel.xpath(price_xpath).get()
material_composition = sel.xpath(composition_xpath).get()
description = sel.xpath(description_xpath).getall()
selling_price = price.split()[0]
currency = price.split()[1]
code = sel.xpath(code_xpath).get()
features = sel.xpath(features_xpath).getall()
images = sel.xpath(image_xpath).getall()

product_description = " ".join([text.strip() for text in description if text.strip()])
features = " ".join(features)

