import requests
from parsel import Selector
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

url = "https://www.petsandfriends.co.uk/collections/dry-dog-food?&sort=PRICE_DESC"

response = requests.get(url,headers=headers)
sel = Selector(response.text)
product_script = sel.xpath('//script[@type="application/ld+json" and contains(., \'"@type": "Product"\')]/text()').get()
data = json.loads(product_script)
pdp_urls = [
    item.get("offers",[{}])[0].get("url")
    for item in data
    ]

######################### PARSER #################################

pdp_url = "https://www.petsandfriends.co.uk/products/orijen-six-fish-grain-free-all-breeds-amp-life-stage-dog-food-11-4kg"

response = requests.get(url=pdp_url,headers=headers)

sel = Selector(response.text)

product_name_xpath = '//h1[@class="c-product__title"]/span/text()'
price_xpath = '//span[@class="c-price-item c-price-item--regular"]/text()'
images_xpath = '//div[@class="c-slider__thumbnail-inner"]/img[contains(@class,"c-slider__image")]/@data-src'
product_description_xpath = '//div[@class="c-accordion__item"][h2[text()="About this product"]]/div[@class="c-accordion__content"]/p/text()'
ingredients_xpath = '//div[@class="c-accordion__item"][h2[text()="Ingredients"]]/div[@class="c-accordion__content"]/p/text()'
nutrition_xpath = '//div[@class="c-accordion__item"][h2[text()="Nutrition"]]/div[@class="c-accordion__content"]/p/text()'
review_xpath = '//div[@class="jdgm-rev-widg__summary-text"]/text()'
rating_xpath = '//div[@id="judgeme_product_reviews"]/div/@data-average-rating'
stock_xpath = '//label[contains(@class, "c-product__stock-label")]/span/text()'
breadcrumb_xpath = '//li/a[@class="c-menu__link"]/text()'
grammage_xpath = '//div[@class="c-price__per"]/text()'
promo_description_xpath = '//div[@class="c-product__subscription-price"]//text()'

product_name = sel.xpath(product_name_xpath).get()
regular_price = sel.xpath(price_xpath).get()
images = sel.xpath(images_xpath).getall()
product_description = sel.xpath(product_description_xpath).getall()
ingredients = sel.xpath(ingredients_xpath).getall()
nutrition = sel.xpath(nutrition_xpath).getall()
review = sel.xpath(review_xpath).get()
rating = sel.xpath(review_xpath).get()
stock = sel.xpath(stock_xpath).get()
breadcrumb = sel.xpath(breadcrumb_xpath).getall()
grammage = sel.xpath(grammage_xpath).get()
promotion_description = sel.xpath(promo_description_xpath).getall()

instock = stock.strip().lower() == "in stock" if stock else False
breadcrumb = " > ".join(breadcrumb)
