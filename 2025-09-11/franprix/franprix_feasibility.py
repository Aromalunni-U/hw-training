import requests
from parsel import Selector
from text_cleaner import clean_price


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

page_no = 1
count = 1

while True:
    
    url = f"https://www.franprix.fr/department/boissons?offset=16&page={page_no}"


    response = requests.get(url=url, headers=HEADERS)
    if response.status_code == 200:
        sel = Selector(response.text)

        pdp_urls = sel.xpath('//a[@class="product-card__title"]/@href').getall()
        pdp_urls = [f"https://www.franprix.fr{url}" for url in pdp_urls]
        
        if not pdp_urls:
            break
        
        for url in pdp_urls:
            print(f"{url} - {count}")
            count += 1
            
        page_no += 1
        
    else:
        print(f"Status code : {response.status_code}")
        
##################### PARSER ###################

# url = "https://www.franprix.fr/promotion/27082025-3383482297050-super-decapant-cuisine-en-promotion"
# url = "https://www.franprix.fr/promotion/27082025-3229820769141-galette-de-mais-chocolat-au-lait-bio-en-promotion"
# url = "https://www.franprix.fr/promotion/27082025-3179071000343-cotes-du-rhone-vin-rose-en-promotion"

# response = requests.get(url=url, headers=HEADERS)
# if response.status_code == 200:
#     sel = Selector(response.text)
    
#     PRODUCT_NAME_XPATH = '//h1[@class="product-page-name"]/text()'
#     BRAND_XPATH = '//h2[contains(@class, "product-page-brand")]/text()'
#     PRICE_PER_KG_XPATH = '//p[contains(text(), "Le kilo") or contains(text(), "litre")]/text()'
#     IMAGE_XPATH = '//picture[@class="block text-body-3 w-full h-full"]//img/@src'
#     INGREDIENT_XPATH = '//div[div[contains(text(), "Ingrédients")]]/div[2]/text()'
#     ALLERGENCE_XPATH = '//div[div[contains(text(), "Allergènes")]]/div[2]/text()'
#     EAN_XPATH = '//div[div[contains(text(), "EAN")]]/div[2]/text()'
#     CATEGORY_XPATH = '//nav//a/text() | //nav//div/text()'
#     PROMO_DESCRIPTION = '//div[@class="absolute bottom-0 left-4 flex items-end gap-1"]//text()'
#     PROMO_START_FROM = '//p[contains(text(), "Valable du")]/text()'
#     COUNTRY_XPATH = '//div[@class="uppercase font-bold"]/p[2]/text()'
#     PROMO_END_DATE = '//div[@class="text-body-1 font-bold"]/text()'
#     LEGAL_NAME_XPATH = '//div[div[contains(text(), "Dénomination légale")]]/div[2]/text()'
#     PRODUCT_DECSRIPTION_XPATH = '//div[div[contains(text(), "Le produit")]]/div[2]/text()'


#     product_name = sel.xpath(PRODUCT_NAME_XPATH).get()
#     brand = sel.xpath(BRAND_XPATH).get()
#     price_per_kg = sel.xpath(PRICE_PER_KG_XPATH).get()
#     image_url = sel.xpath(IMAGE_XPATH).get()
#     ingredinets = sel.xpath(INGREDIENT_XPATH).get()
#     allergen = sel.xpath(ALLERGENCE_XPATH).get()
#     ean = sel.xpath(EAN_XPATH).get()
#     category_path = sel.xpath(CATEGORY_XPATH).getall()
#     promo_description = sel.xpath(PROMO_DESCRIPTION).getall()
#     promo_start_date = sel.xpath(PROMO_START_FROM).get()
#     country = sel.xpath(COUNTRY_XPATH).get()
#     promo_end_date = sel.xpath(PROMO_END_DATE).get()
#     legal_name  =sel.xpath(LEGAL_NAME_XPATH).get()
#     product_description = sel.xpath(PRODUCT_DECSRIPTION_XPATH).get()
    

#     product_name = product_name.strip() if product_name else ""
#     brand = brand.strip() if brand else ""
#     price_per_kg = price_per_kg if price_per_kg else ""
#     allergen = allergen.strip() if allergen else ""
#     ingredinets = ingredinets.strip() if ingredinets else ""
#     ean = ean.strip() if ean else ""
#     category_path = " > ".join([path.strip() for path in category_path])
#     promo_description = " ".join([des.strip() for des in promo_description if des.strip()])


#     nutrition = {}
#     rows = sel.xpath('//div[div[contains(text(), "nutritionnelles")]]//div')

#     for row in rows:
#         key = row.xpath('./div[1]//text()').get()
#         value = row.xpath('./div[2]//text()').get()

#         if key and value:
#             nutrition[key.strip()] = value.strip()
    
# else:
#     print(f"Status code : {response.status_code}")
    
