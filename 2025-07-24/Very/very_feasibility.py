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


################## CRAWLER ##############

category_url = "https://www.very.co.uk/browse/mens-jeans"
page_no = 1

while True:
    url = category_url if page_no == 1 else f"{category_url}?page={page_no}"

    res = requests.get(url=url, headers=HEADERS)
    if res.status_code == 200:
        sel = Selector(res.text)

        pdp_urls = sel.xpath('//a[@data-testid="fuse-complex-product-card__link"]/@href').getall()
        pdp_urls = [f"https://www.very.co.uk{url}" for url in pdp_urls]

        if not pdp_urls:
            break

        for link in pdp_urls:
            print(link)

        page_no += 1

    else:
        print(f"Status code: {res.status_code}")
        break

#################### PARSER ######################


url = "https://www.very.co.uk/levis-555-relaxed-straight-fit-utility-jeans-everyday-goods-light-blue/1600994653.prd"

res = requests.get(url=url, headers= HEADERS)
if res.status_code == 200:
    sel = Selector(res.text)

    PRODUCT_NAME  = '//span[@data-testid="product_title"]/text()'
    BRAND_XPATH = '//span[@data-testid="product_brand"]/text()'
    PRICE_XPARTH = '//p[@data-testid="product_price_current"]/text()'
    PRICE_WAS_XPATH = '//p[@data-testid="product_price_previous"]/text()'
    REVIEW_XPATH = '//a[@data-testid="rating-and-reviews-summary_rating__review"]/text()'
    RATING_XPATH = '//span[contains(text(), "out of 5 stars")]/text()'
    IMAGE_XPATH = '//picture/img/@src'
    PRODUCT_DESCRIPTION_XPATH = '//div[@data-testid="product_description_body"]/text()'
    EAN_XPATH = '//p[@data-testid="product_description_ean"]/text()'
    SIZE_XPATH = '//label[contains(@for, "size")]/span/text()'


    product_name =  sel.xpath(PRODUCT_NAME).get()
    brand = sel.xpath(BRAND_XPATH).get()
    selling_price = sel.xpath(PRICE_XPARTH).get()
    price_was = sel.xpath(PRICE_WAS_XPATH).get()
    review = sel.xpath(REVIEW_XPATH).get()
    rating = sel.xpath(RATING_XPATH).get()
    image = sel.xpath(IMAGE_XPATH).getall()
    product_description = sel.xpath(PRODUCT_DESCRIPTION_XPATH).get()
    ean = sel.xpath(EAN_XPATH).get()
    size = sel.xpath(SIZE_XPATH).getall()