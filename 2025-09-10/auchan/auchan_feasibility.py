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

headers = {
    'accept': 'application/crest',
    'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'x-crest-renderer': 'search-renderer',
    'x-requested-with': 'XMLHttpRequest',
}


################### CRAWLER ##############################

page_no = 1
category_id = 'n010809'

while True:
    params = {
        'categoryId': category_id,
        'page': page_no,
        'x-cms-page-template': 'PRODUCT_LIST_PAGE_TEMPLATE',
        'x-cms-page-type': 'CATEGORY',
        'x-cms-ua-device': 'MOBILEFIRST',
        'x-cms-category': category_id,
    }
    url = 'https://www.auchan.fr/search-infinite'

    response = requests.get(url=url, params=params, headers=headers)
    if response.status_code == 200:
        sel = Selector(response.text)
        
        pdp_urls = sel.xpath('//a[@autotrack-event-action="productdetails"]/@href').getall()
        pdp_urls = [f"https://www.auchan.fr{url}" for url in pdp_urls]
        
        if not pdp_urls:
            break

        for url in pdp_urls:
            print(url)
        
        page_no += 1
    else:
        print(f"Status code : {response.status_code}")
        break
    
#################### PARSER #############################



url = "https://www.auchan.fr/le-petit-versaillais-yaourt-nature-sur-lit-d-abricot/pr-C1171796"
url = "https://www.auchan.fr/mon-fromager-appenzeller-extra-fort-6-mois-d-affinage/pr-C1618995"

response = requests.get(url=url, headers=HEADERS)

if response.status_code == 200:
    sel = Selector(response.text)
    
    PRODUCT__NAME_XPATH = '//h1/text()'
    DESCRIPTION_XPATH = '//div[h5[contains(text(), "Description")]]//span/text()'
    COUNTRY_XPATH = '//div[h5[contains(text(), "Pays de fabrication")]]//span/text()'
    IMAGE_XPATH = '//div[contains(@class, "product-zoom__item")]/img/@src'
    INGREDIENTS_XPATH = '//div[h5[contains(text(), "Ingrédients")]]//span/text()'
    LEGAL_NAME_XPATH = '//div[h5[contains(text(), "Dénomination légale de vente")]]//span/text()'
    PRODUCT_CODE  = '//div[span[contains(text(), "EAN")]]/div/text()'
    PACK_SIZE__XPATH = '//span[@class="product-attribute"]/text()'
    CATEGORY_XPATH = '//span[@class="site-breadcrumb__item"]/a/text()'
    
    
    product_name = sel.xpath(PRODUCT__NAME_XPATH).get()
    product_description = sel.xpath(DESCRIPTION_XPATH).get()
    country = sel.xpath(COUNTRY_XPATH).get()
    image = sel.xpath(IMAGE_XPATH).get()
    ingredient = sel.xpath(INGREDIENTS_XPATH).get()
    legal_name = sel.xpath(LEGAL_NAME_XPATH).get()
    product_code = sel.xpath(PRODUCT_CODE).get()
    pack_size = sel.xpath(PACK_SIZE__XPATH).get()
    category_path = sel.xpath(CATEGORY_XPATH).getall()
    
    nutrition = {}
    rows = sel.xpath('//table[@id="nutritionals_0"]//tbody/tr')
    for row in rows:
        key = row.xpath('./td[1]//text()').get()
        value = row.xpath('./td[2]//text()').get()
        if key and value:
            nutrition[key.strip()] = value.strip()
            

########### Second request ##########



url = 'https://www.auchan.fr/product-page'

cookies = {
    'lark-journey': 'c8ba7c98-15c2-4eaf-80ba-97367e274adb',
}

params = {
    'productId':'C1264653'
}

headers['x-crest-renderer'] = 'product-renderer'

response = requests.get(
    url=url,
    params=params,
    cookies=cookies,
    headers=headers
)

sel = Selector(response.text)

PRICE_PER_PACK_XPATH = '//meta[@itemprop="price"]/@content'
ALLERGEN_DIETARY_CLAIMS_XPATH = '//span[contains(text(), "Allergènes")]/following-sibling::span/text()'
PRICE_PER_UNIT_XPATH = '//div[contains(@class,"product-price--smaller")]/span/text()'
PROMOTION_END_DATE_XPATH = '//div[@id="discount-end-date"]//p/text()'
PROMOTION_DESCRIPTION_XPATH = '//span[@class="product-discount-label"]/text()'
BRAND_XPATH = '//meta[@itemprop="brand"]/@content'


price_per_pack = sel.xpath(PRICE_PER_PACK_XPATH).get()
allergen_dietary_claims = sel.xpath(ALLERGEN_DIETARY_CLAIMS_XPATH).get()
price_per_unit = sel.xpath(PRICE_PER_UNIT_XPATH).get()
promotion_end_date = sel.xpath(PROMOTION_END_DATE_XPATH).get()
promotion_description = sel.xpath(PROMOTION_DESCRIPTION_XPATH).get()
brand = sel.xpath(BRAND_XPATH).get()
