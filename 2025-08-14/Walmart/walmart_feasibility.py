import requests
import json
from urllib.parse import urlparse
from parsel import Selector


HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
    'cache-control': 'no-cache',
    'downlink': '2',
    'dpr': '1.25',
    'pragma': 'no-cache',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
}

def nutrient_and_vitamin(data):
    key = data.get("name")
    amount = data.get("amount", "")
    dvp = data.get("dvp")
    
    amount = amount if amount else ""
    dvp = dvp if dvp else ""
    value = f"{amount} {dvp}".strip()
    
    return key, value    

#################### CRAWLER ############################


page_no = 1
category_url = "https://www.walmart.com/shop/deals/flash-deals-electronics?povid=ETS_NA_NA_NA_ITEMCRS_FLDL_CP_3944_TechFlashDeals"

url_parts = urlparse(category_url).path.strip("/").split("/")
url_parts = "&seo=".join(url_parts[1:])

while True:
        
    page_url = f"{category_url}&seo={url_parts}&page={page_no}&affinityOverride=default"
    
    response = requests.get(url=page_url, headers=HEADERS)
    if response.status_code == 200:

        sel = Selector(response.text)
        json_ld = sel.xpath('//script[contains(text(),"OfferCatalog")]/text()').get()

        if not json_ld:
            break

        try:
            data = json.loads(json_ld)
        except:
            break

        products = data.get("itemListElement", [])
        if not products:
            break

        pdp_urls = [f"https://{p.get('url', '').lstrip('/')}" for p in products if p.get("url")]
        for url in pdp_urls:
            print(url)
        page_no += 1
        
    else:
        print(f"Status code  {response.status_code}")

################ PARSER ###################


url = "https://www.walmart.com/ip/Totino-s-Ultimate-Pizza-Extra-Cheese-Frozen-Pizza-Frozen-Snacks-10-69-oz/15205561102?adsRedirect=true"


response = requests.get(url=url, headers=HEADERS)
if response.status_code == 200:
    sel = Selector(response.text)

    PRODUCT_NAME_XPATH = '//h1/text()'
    SELLING_PRICE_XPATH = '//span[@itemprop="price"]/text()'
    REGULAR_PRICE_XPATH = '//span[@data-seo-id="strike-through-price"]/text()'
    IMAGE_XPATH = '//div[@class="relative db"]/img/@src'
    RATING_XPATH = '//span[@class="f7 ph1"]/text()'
    REVIEW_XPATH = '//a[@itemprop="ratingCount"]/text()'
    INGREDIENTS_XPATH = '//h3[contains(text(), "Ingredients")]/following-sibling::p/text()'
    SCRIPT_DATA = '//script[@id="__NEXT_DATA__"]/text()'
    PROMO_DESCRIPTION_XPATH = '//div[@data-testid="dollar-saving"]//text()'


    product_name = sel.xpath(PRODUCT_NAME_XPATH).get()
    selling_price = sel.xpath(SELLING_PRICE_XPATH).get()
    regular_price = sel.xpath(REGULAR_PRICE_XPATH).get()
    image = sel.xpath(IMAGE_XPATH).get()
    rating = sel.xpath(RATING_XPATH).get()
    review = sel.xpath(REVIEW_XPATH).get()
    ingredients = sel.xpath(INGREDIENTS_XPATH).get()
    promotion_description = sel.xpath(PROMO_DESCRIPTION_XPATH).get()
    

    json_ld = sel.xpath(SCRIPT_DATA).get()
    data = json.loads(json_ld)


    product = data.get("props", {}).get("pageProps", {}).get("initialData", {}).get("data", {})
    warranty = (product.get("idml", {}).get("warranty") or {}).get("information", "")
    product_description = product.get("product", {}).get("shortDescription", "")
    
    instructionforuse = ", ".join([
        d.get("value", "") for d in product.get("idml", {}).get("directions", [])
    ])

    nutrients_data = product.get("idml", {}).get("nutritionFacts", {}).get("keyNutrients", {}).get("values", [])
    
    vitamins_data =  (
        ((product.get("idml") or {}).get("nutritionFacts") or {}).get("vitaminMinerals") or {}
    ).get("childNutrients", [])
    
    nutrients = {}

    for data in nutrients_data:
        main = data.get("mainNutrient", {})
        child_nutrients = data.get("childNutrients", [])

        if main:
            key, value = nutrient_and_vitamin(main)
            nutrients[key] = value

        if child_nutrients:
            for nutrient in child_nutrients:
                key, value = nutrient_and_vitamin(nutrient)
                nutrients[key] = value
        
    vitamins = {}

    for vitamin in vitamins_data:
        key, value = nutrient_and_vitamin(vitamin)
        vitamins[key] = value


else:
    print(f"Status code :{response.status_code}")
