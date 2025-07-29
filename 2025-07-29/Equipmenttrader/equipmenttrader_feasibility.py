import requests
from parsel import Selector
import json

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Priority': 'u=0, i',
}

############## CATEGORY #####################

url = "https://www.equipmenttrader.com/Equipment-by-Category/equipment-for-sale?vrsn=links&format=category"

res = requests.get(url = url, headers= HEADERS)
print(res)

sel = Selector(res.text)

category_url = sel.xpath('//div[@class="browseContainer"]//a/@href').getall()

category_url = [f"https://www.equipmenttrader.com{url}" for url in category_url]

#################### CRAWLER #############


def scrap_item(response):
    sel = Selector(response.text)
    script_data = sel.xpath('//script[@type="application/ld+json" and not(contains(text(), "BreadcrumbList"))]/text()').get()
    
    if not script_data:
        return False

    data = json.loads(script_data)
    products = data.get("offers",{}).get("offers",[])


    pdp_urls = [product.get("url","") for product in products]

    for url in pdp_urls:
        print(url)
    
    return True if pdp_urls else False




min_price = 1
max_price = 10000
zip_code = 23462
category_url = "https://www.equipmenttrader.com/Forklifts/equipment-for-sale?category=Forklifts%7C2000234"

while True:

    params = f"&price={min_price}%3A{max_price}&zip={zip_code}&radius=10000"
    url = f"{category_url}{params}&page=1"

    res = requests.get(url=url, headers=HEADERS)
    sel = Selector(res.text)

    total_count = sel.xpath('//span[@class="inventory-count bold"]/text()').get()
    total_count = int(total_count.replace(",", ""))

    print(f"Checking range: {min_price} - {max_price} | Count : {total_count}")


    if total_count <= 380:
        page_no = 1

        while page_no <= 10:

            page_url = f"{category_url}{params}&page={page_no}"
            res = requests.get(page_url, headers=HEADERS)

            available = scrap_item(res)
            if not available:
                break  

            page_no += 1

        min_price = max_price
        max_price += 10000

    else:
        max_price = (min_price + max_price) // 2

   
    

################ PARSER ################

url = "https://www.equipmenttrader.com/listing/2022-KUBOTA-SVL97-2+Skidsteer-5036704670#sid=740617"

res = requests.get(url=url, headers= HEADERS)
print(res)

sel = Selector(res.text)

PRICE_XPATH = '//span[@id="addetail-price-detail"]/text()'
IMAGE_XPATH = '//link[@as="image"]/@href'
SPEC_XPATH = '//div[@id="info-list-seller"]/ul/li'
NAME_XPATH = '//div[@class="dealer-name"]/span[2]/text()'
PHONE_XPATH = '//div[span[@class="fas fa-phone"]]/text()[normalize-space()]'
DESCRIPTION_XPATH = '//div[@class="list-unstyled descriptionText clearBoth"]//text()'

price = sel.xpath(PRICE_XPATH).get()
image = sel.xpath(IMAGE_XPATH).get()
spec_data = sel.xpath(SPEC_XPATH)
name = sel.xpath(NAME_XPATH).get()
phone = sel.xpath(PHONE_XPATH).get()
description = sel.xpath(DESCRIPTION_XPATH).getall()


description = ", ".join(description) if description else ""
specification = {}

for spec in spec_data:
    key = spec.xpath('.//div/h3/span[1]/text()').get()
    value = spec.xpath('.//div/h3/span[2]/text()').get()
    if key:
        specification[key.replace(":","").strip()] = value.strip() if value else ""


