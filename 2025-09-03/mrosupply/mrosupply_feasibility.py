import requests
from parsel import Selector
from datetime import datetime



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

######################### CRAWLER ###########################

page_no = 1

while True:
    
    url = f"https://www.mrosupply.com/electric-motors/ac-motors/?page={page_no}"

    response = requests.get(url=url, headers=HEADERS)
    sel = Selector(response.text)
    if response.status_code == 200:
        
        pdp_urls = sel.xpath('//a[contains(@class, "product-title")]/@href').getall()
        pdp_urls = [f"https://www.mrosupply.com/{url}" for url in pdp_urls]
        for url in pdp_urls:
            print(url)
            
        page_no += 1
    
    else:
        print(f"Status code : {response.status_code}")
        break


############################# PRASER ##############################

url = "https://www.mrosupply.com/fleet-and-vehicle-maintenance/108612_d150_dixon/"
url = "https://www.mrosupply.com/electric-motors/25344_em3615t_baldor/"

response = requests.get(url=url, headers=HEADERS)
if response.status_code == 200:
    sel = Selector(response.text)
    
    MANUFACTURER_NAME_XPATH = ""
    BRAND_NAME_XPATH = '//a[@class="js-brand-name"]/text()'
    VENDOR_SELLER_PART_NUMBER_XPATH = '//div[p[contains(text(), "SKU")]]/following-sibling::div/p/text()' 
    ITEM_NAME_XPATH = '//h1/text()'
    FULL_PRODUCT_DESCRIPTION_XPATH = '//div[@class="m-accordion--item--body"]//text()'
    PRICE_XPATH = '//p[contains(@class,"price")]/text()'
    UPC_XPATH = '//div[p[contains(text(), "UPC")]]/following-sibling::div/p/text()'        
    MODEL_NUMBER_XPATH = '//p[@class="modelNo"]/text()'
    PRODUCT_CATEGORY_XPATH = '//ul[@class="m-breadcrumbs-list"]/li[last()]//span/text()'
    IMAGE_XPATH = '//img[@class="js-magnify"]/@src'
    DATE_CRAWLED = datetime.now().strftime("%Y-%m-%d")

    manufacturer_name = sel.xpath(MANUFACTURER_NAME_XPATH).get()
    brand_name = sel.xpath(BRAND_NAME_XPATH).get()
    vendor_seller_part_number = sel.xpath(VENDOR_SELLER_PART_NUMBER_XPATH).get()
    item_name = sel.xpath(ITEM_NAME_XPATH).get()
    full_description = sel.xpath(FULL_PRODUCT_DESCRIPTION_XPATH).getall()
    price = sel.xpath(PRICE_XPATH).get()
    upc = sel.xpath(UPC_XPATH).get()
    model_number = sel.xpath(MODEL_NUMBER_XPATH).get()
    product_category = sel.xpath(PRODUCT_CATEGORY_XPATH).get()
    image = sel.xpath(IMAGE_XPATH).get()
    
    
    
else:
    print(f"Status code : {response.status_code}")
