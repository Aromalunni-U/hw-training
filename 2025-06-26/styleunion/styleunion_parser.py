import requests
from parsel import Selector


urls = [
    "https://styleunion.in/collections/womens-tops/products/regular-fit-solid-crop-top-ywto00076", 
    "https://styleunion.in/collections/womens-tops/products/regular-fit-solid-shirt-wsh00070", 
    "https://styleunion.in/collections/womens-tops/products/flare-fit-floral-print-tie-up-neck-top-it00046", 
    "https://styleunion.in/collections/womens-tops/products/regular-fit-solid-t-shirt-lete00018"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
}

for url in urls:
    response = requests.get(url,headers= HEADERS)
    sel = Selector(response.text)

    PRODUCT_NAME_XPATH = '//h1[@class="product__section-title product-title"]/text()'
    REGULAR_PRICE_XPATH = '//span[@class="price-item price-item--regular"]/text()'
    COLOR_XPATH = '//span[@class="swatches__color-name"]/text()'
    SKU_XPATH = '//span[@id="variantSku"]/text()'
    SIZE_XPATH = '//label[@class="swatches__form--label"]/text()'
    CARE_INSTRUCTIONS_TEXT = '//div[h3[text()="Wash and Care"]]/following-sibling::div/text()'
    CARE_INSTRUCTIONS_LIST = (
        '//div[h3[text()="Wash and Care"]]/following-sibling::div/ul/li/text()'
        '|'
        '//div[h3[text()="Wash and Care"]]/following-sibling::div/li/text()'
    )
    FABRIC_TYPE_XPATH =  (
        '//strong[text()="Fabric Type:" or text()="Fabric:"]/following-sibling::text()'
        '|'
        '//li/b[text()="Fabric type:"]/following-sibling::text()'
    )
    PATTERN_XPATH = (
        '//strong[text()="Pattern:"]/following-sibling::text()'
        '|'
        '//li/b[text()="Pattern:"]/following-sibling::text()'
        '|'
        '//b[text()="Pattern:"]/following-sibling::text()'
    )
    CLOTHING_FIT_XPATH = (
        '//strong[text()="Fit:" or text()="Fit Type:"]/following-sibling::text()'
        '|'
        '//li/b[text()="Fit:" or text()="Fit Type:"]/following-sibling::text()'
        '|'
        '//b[text()="Fit:" or text()="Fit Type:"]/following-sibling::text()'
    )
    POCKET_XPATH = '//strong[text()="Pockets:"]/following-sibling::text()'

    SLEEVE_TYPE_XPATH = (
        '//strong[text()="Sleeve Type:"]/following-sibling::text()'
        '|'
        '//li/b[text()="Sleeve Type:"]/following-sibling::text()'
        '|'
        '//b[text()="Sleeve Type:"]/following-sibling::text()'
    )
    COLLAR_TYPE_XPATH = (
        '//strong[contains(text(),"Neck") or contains(text(), "Collar")]/following-sibling::text()'
        '|'
        '//b[contains(text(),"Neck") or contains(text(), "Collar")]/following-sibling::text()'
    )

    CLOATHING_LENGTH_XPATH = (
        '//b[text()="Length:"]/following-sibling::text()'
        '|'
        '//strong[text()="Length:"]/following-sibling::text()'
    )

    RATING_XPATH = '//div[@class="jdgm-prev-badge"]/@data-average-rating'
    REVIEW_XPATH = '//div[@class="jdgm-prev-badge"]/@data-number-of-reviews'
    DESCRIPTION_XPATH = '//h3[text()="Description"]/following::div[contains(@class,"acc__panel")][1]/text()'

    IMAGE_XPATH = '//div[@class="box-ratio "]/img/@src'

    product_name = sel.xpath(PRODUCT_NAME_XPATH).get()
    regular_price = sel.xpath(REGULAR_PRICE_XPATH).get() 
    color = sel.xpath(COLOR_XPATH).getall()
    sku = sel.xpath(SKU_XPATH).get()
    size = sel.xpath(SIZE_XPATH).getall()
    care_instructions = sel.xpath(CARE_INSTRUCTIONS_TEXT).get().strip()
    fabric_type = sel.xpath(FABRIC_TYPE_XPATH).get()
    pattern = sel.xpath(PATTERN_XPATH).get()
    clothing_fit = sel.xpath(CLOTHING_FIT_XPATH).get()
    pocket = sel.xpath(POCKET_XPATH).get()
    sleeve_type = sel.xpath(SLEEVE_TYPE_XPATH).get()
    collar_type = sel.xpath(COLLAR_TYPE_XPATH).get()
    product_description = sel.xpath(DESCRIPTION_XPATH).get()
    images = sel.xpath(IMAGE_XPATH).getall()
    clothing_length = sel.xpath(CLOATHING_LENGTH_XPATH).get()

    rating = sel.xpath(RATING_XPATH).get()
    review = sel.xpath(REVIEW_XPATH).get()

    if not care_instructions:
        care_instructions = sel.xpath(CARE_INSTRUCTIONS_LIST).getall()
        care_instructions = " ".join(care_instructions)

    regular_price = regular_price.strip().replace("₹","") if regular_price else ""
    size = [i.strip() for i in size if i.strip()]
    fabric_type = fabric_type.strip() if fabric_type else ""
    pattern = pattern.strip() if pattern else ""
    pocket = pocket.strip() if pocket else ""
    clothing_fit = clothing_fit.strip() if clothing_fit else ""
    sleeve_type = sleeve_type.strip() if sleeve_type else ""
    collar_type = collar_type.strip() if collar_type else ""
    product_description = product_description.strip() if product_description else ""

