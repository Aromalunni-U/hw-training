import json
import requests
from tqdm import tqdm
import logging
from parsel import Selector
from urllib.parse import urljoin
from aldi_plp import get_products_link

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M"
)

def parse_product(product_links, url):
    try:
        for link in tqdm(product_links):
                product_url = urljoin(url,link)
                product_response = requests.get(product_url)

                if product_response.status_code == 200:

                    product_selector = Selector(product_response.text)
                    product_name = product_selector.xpath(
                        "//h1[@class='product-details__title']/text()"
                    ).get().split(",")[0].strip()

                    breadcrumb= product_selector.xpath("//nav[@aria-label='Breadcrumb']//a/text()").getall()
                    raw_price = product_selector.xpath("//span[@class='base-price__regular']/span/text()").get()

                    image = product_selector.xpath(
                        "//div/img[contains(@class,'base-image') and contains(@class,'zoom-on-hover__image')]/@src"
                    ).get()

                    product_id = product_selector.xpath(
                        "//button[@data-test='product-add-cart']/@data-mn"
                    ).get().split("-")[-1]
                    product_quantity = product_selector.xpath(
                        "//span[@data-test='product-details__unit-of-measurement']/text()"
                    ).get()

                    origin = product_selector.xpath(
                        "//div[@data-test='base-accordion-item__content-inner']/text()"
                    ).get() or "N/A"

                    product_description = product_selector.xpath(
                        "//div[@class='show-more__content']/div[contains(@class,'base-rich-text')]/text()"
                    ).get() or "no description"

                    if product_quantity:
                         product_quantity = product_quantity.strip()
                    else:
                         product_quantity = product_selector.xpath(
                            "//h1[@class='product-details__title']/text()"
                        ).get().split(",")[1].strip()

                    if raw_price:
                         price = raw_price[1:]
                         currency = raw_price[0]

                    yield {
                        "product_name": product_name,
                        "product_link": product_url,
                        "product_id": product_id,
                        "product_quantity":product_quantity,
                        "price": price,
                        "currency":currency,
                        "origin": origin,
                        "image": image,
                        "product_description": product_description,
                        "breadcrumb": breadcrumb,
                    }
                else:
                     logging.error("status code:", product_response.status_code)
    except Exception as e:
        logging.error(f"An error occurred: {e}")


url = "https://www.aldi.us/products/fresh-produce/fresh-fruit/k/89" 
file_path = "2025-05-02/aldi.json"

product_links = get_products_link(url)
logging.info(f"Total products: {len(product_links)}")
products = list(parse_product(product_links,url))

with open(file_path,"w") as file:
    json.dump(products, file, indent=4)

logging.info("Completed successfully")