import requests
from parsel import Selector
import json
import re

url = "https://www.kiwoko.com/sitemap-products_0.xml"

response = requests.get(url=url)
pdp_urls = re.findall(r'<loc>(.*?)</loc>',response.text)

################## PARSER #################

pdp_url = "https://www.kiwoko.com/perros/comida-para-perros/pienso-seco-para-perros/pienso-de-pescado/true-origins-pure-salmon-pienso-para-perros/TRU70969_M.html"


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

response = requests.get(pdp_url, headers=headers)

if response.status_code == 200:
    sel = Selector(text=response.text)
    script_text = sel.xpath('//script[@type="application/ld+json"]/text()').get()

    product_data = json.loads(script_text)

    product_name = product_data.get("name","")
    product_id = product_data.get("productID","")
    brand = product_data.get("brand", {}).get("name")
    rating = product_data.get("aggregateRating", {}).get("ratingValue")
    review = product_data.get("aggregateRating", {}).get("ratingCount")
    product_Description = product_data.get("description","")

    current_price_xpath = '//span[@class="isk-attribute-card__price"]/text()'
    price_per_unit_xpath = '//span[@class="product-page-action__pum"]/text()'
    grammage_xpath = '//strong[contains(@class,"variation-attribute__selected")]/text()'
    promo_description_xpath = '//div[@class="isk-promo-callout__header"]/span/text()'
    images_xpath = '//button[@class="product-page-gallery__img-button"]/img/@src'
    breadcrumb_xpath = '//span[@class="js-breadcrumbs-item"]/text()'

    current_price = sel.xpath(current_price_xpath).get()
    price_per_unit = sel.xpath(price_per_unit_xpath).get()
    grammage = sel.xpath(grammage_xpath).get()
    promotion_description = sel.xpath(promo_description_xpath).getall()
    images = sel.xpath(images_xpath).getall()
    breadcrumb = sel.xpath(breadcrumb_xpath).getall()

    breadcrumb = " > ".join([b.strip() for b in breadcrumb])

