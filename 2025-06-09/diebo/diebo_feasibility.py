import requests
from parsel import Selector
import re
from datetime import datetime

HEADERS = {
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

############################### CRAWLER #########################################

search_url = "https://www.diebo.nl/assortiment?q={}&action=getAjaxSearchArtikelen"

for ean in ean_list:
    response = requests.get(search_url.format(ean),headers=HEADERS)
    sel = Selector(response.text)
    if response.status_code == 200:
        links = sel.xpath("//a[@class='full-link']/@href").getall()
        if links:
            links = ["https://www.diebo.nl/" + url for url in links]
            print(links)


############################### PARSER #########################################

pdp_url = "https://www.diebo.nl/hond/hondenbrokken/wellness-core-hondenvoer-small-original-1.5-kg"

response = requests.get(pdp_url,headers=HEADERS)
sel = Selector(response.text)

product_name_xpath = "//h1[@class='forix-product__title']/text()"
price_xpath = "//span[contains(@class,'forix-product__price')]/text()"
price_was_xpath = "//span[@class = 'forix-product__price forix-product__price--actieprijs']/text()"
currency_xpath = "//span[@class='forix-product__valuta']/text()"
description_xpath = "//div[@class='forix-product__desc-short']/text()"
breadcrumb_xpath = "//li[@itemprop='itemListElement']/a/span/text()"
images_xpath = "//figure[contains(@class,'gallery-pager__image')]/img/@src"
barcode_xpath = "//td[contains(text(), 'Barcode')]/following-sibling::td[1]/text()"
netweight_xpath = "//td[contains(text(), 'Maat of inhoud')]/following-sibling::td[1]/text()"
composition_xpath = "//strong[contains(text(),'Samenstelling')]/following-sibling::text()[1]"
valid_upto_xpath = "//div[@class='product-highlight-enddate']/small/text()"
instock_xpath = "//div[@class='label-stock']/span/text()"


product_name = sel.xpath(product_name_xpath).get()
current_price = sel.xpath(price_xpath).get()
price_was = sel.xpath(price_was_xpath).get()
currency = sel.xpath(currency_xpath).get()
product_description = sel.xpath(description_xpath).get()
breadcrumb = sel.xpath(breadcrumb_xpath).getall()
images = sel.xpath(images_xpath).getall()
barcode = sel.xpath(barcode_xpath).get()
netweight = sel.xpath(netweight_xpath).get()
material_composition = sel.xpath(composition_xpath).get()
valid_upto = sel.xpath(valid_upto_xpath).get()
instock = sel.xpath(instock_xpath).get()

product_name = " ".join(product_name.split()[:-2])
price_was = price_was if price_was else 0
product_description = product_description.strip() if product_description else ""
breadcrumb = " > ".join(breadcrumb)
barcode = barcode.strip() if barcode else ""
netweight = netweight.strip() if netweight else ""
material_composition = material_composition.strip() if material_composition else ""

if valid_upto:
    date = re.search(r"\d{2}-\d{2}-\d{4}", valid_upto)
    date = datetime.strptime(date.group(), "%d-%m-%Y")
    valid_upto = date.strftime("%Y-%m-%d")
else:
    valid_upto = ""

instock = True if instock else False

