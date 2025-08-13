import requests
from parsel import Selector


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

############### CATEGORY #########################

url = "https://www.cleverleben.at/produktauswahl"

response = requests.get(url=url, headers=HEADERS)
sel = Selector(response.text)

urls = sel.xpath('//a[@data-teaser-group="marketing"]/@href').getall()
urls = [f"https://www.cleverleben.at{url}" for url in urls]

for url in urls:
    response = requests.get(url=url, headers=HEADERS)
    if response.status_code == 200:
        sel = Selector(response.text)

        category_urls = sel.xpath('//a[@data-teaser-group="marketing"]/@href').getall()
        category_urls = [f"https://www.cleverleben.at{url}" for url in category_urls]
        
        for url in category_urls:
            print(url)
        



##################### CRAWLER ##########################

category_url = "https://www.cleverleben.at/produkte/brot-und-backwaren-10551"
url = category_url

page_no = 1
while True:
    response = requests.get(url=url, headers=HEADERS)
    if response.status_code == 200:
        sel = Selector(response.text)

        pdp_url = sel.xpath('//a[@data-test="product-tile-link"]/@href').getall()

        if not pdp_url:
            break

        pdp_url = [f"https://www.cleverleben.at{url}" for url in pdp_url]

        for i in pdp_url:
            print(i)

        url = f"{category_url}?page={page_no}"
        page_no += 1

    else:
        print(f"Status code : {response.status_code}")
        break

##################### PARSER ####################

url = "https://www.cleve2rleben.at/produkt/marillenroulade-400g-2722413"

response = requests.get(url=url, headers=HEADERS)
if response.status_code == 200:
    sel = Selector(response.text)

    PRODUCT_NAME_XPATH = '//h1/text()'
    SELLING_PRICE_XPATH = '//div[contains(@class, "text-regular-price")]/text()'
    IMAGE_XPATH = '//img[@data-test="product-detail-image"]/@src'
    NUTRITIONS_XPATH = '//table[contains(@class, "nutrition-table")]/tbody/tr'
    PRODUCT_DESC_XPATH = '//div[contains(@class, "description-short")]/text()'
    INGREDIENT_XPATH = '//div[contains(text(), "Zutaten")]/following-sibling::div//text()'
    ALLERGENS_XPATH = '//div[contains(text(), "Allergene")]/following-sibling::div//text()'

    product_name = sel.xpath(PRODUCT_NAME_XPATH).get()
    selling_price = sel.xpath(SELLING_PRICE_XPATH).get()
    image = sel.xpath(IMAGE_XPATH).get()
    product_description = sel.xpath(PRODUCT_DESC_XPATH).get()
    ingredients = sel.xpath(INGREDIENT_XPATH).get()
    allergens = sel.xpath(ALLERGENS_XPATH).getall()

    nutritions = {}
    table_rows = sel.xpath(NUTRITIONS_XPATH)
    for row in table_rows:
        key = row.xpath('./th/text()').get()
        value = row.xpath('./td//text()').getall()
        nutritions[key.strip()] = " ".join(value).replace("\xa0", "").strip()

    currency = "EUR" if "€" in selling_price else ""
    selling_price = (
        selling_price.replace("€", "").replace(",", ".").strip()
        if selling_price else ""
    )
    allergens = " ".join(allergens) if allergens else ""


else:
    print(f"Status code : {response.status_code}")