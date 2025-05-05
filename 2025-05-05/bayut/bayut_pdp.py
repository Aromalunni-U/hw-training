import csv
import json
import requests
from tqdm import tqdm
from parsel import Selector
from urllib.parse import urljoin
from bayut_plp import get_product_links
from settings import CSV_FILE_PATH, JSON_FILE_PATH, BASE_URL


def get_product(product_links, url):

    try:
        for link in tqdm(product_links):
            property_url = urljoin(url, link)
            response = requests.get(property_url)

            if response.status_code == 200:
                selector = Selector(response.text)

                currency = selector.xpath("//span[@aria-label='Currency']/text()").get()
                price = selector.xpath("//span[@aria-label='Price']/text()").get()
                image = selector.xpath(
                    "//picture[@class='a659dd2e']/img[@role='presentation' and @class='_5a31e77d e6a91003']/@src"
                ).getall()

                location = selector.xpath(
                "//div[@class='e4fd45f0' and @aria-label='Property header']/text()"
                ).get()

                area = selector.xpath(
                    "//span[@aria-label='Area']//span/text()"
                ).get()

                property_type = selector.xpath(
                    "//span[@aria-label='Type']/text()"
                ).get()

                beds = selector.xpath(
                    "//span[@aria-label='Beds']/span[@class='_140e6903']/text()"
                ).get().split()[0]

                baths = selector.xpath(
                    "//span[@aria-label='Baths']/span[@class='_140e6903']/text()"
                ).get().split()[0]

                breadcrumb = selector.xpath(
                    "//div[@aria-label='Breadcrumb']//span[@aria-label='Link name']/text()"
                ).getall()

                reference_no = selector.xpath(
                    "//ul[@class='_3dc8d08d']/li/span[@aria-label='Reference']/text()"
                ).get().split()[-1].strip()

                furnishing = selector.xpath(
                    "//ul[@class='_3dc8d08d']/li/span[@aria-label='Furnishing']/text()"
                ).get() or "N/A"

                added_on = selector.xpath(
                    "//ul[@class='_3dc8d08d']/li/span[@aria-label='Reactivated date']/text()"
                ).get() or "N/A"

                purpose = selector.xpath(
                    "//ul[@class='_3dc8d08d']/li/span[@aria-label='Purpose']/text()"
                ).get() or "N/A"

                trucheck_date = selector.xpath(
                    "//li[@aria-label='Property TruCheck verification date']//span[@aria-label='Trucheck date']/text()"
                ).get()

                yield {
                    "property_link": property_url,
                    "price": price,
                    "currency": currency,
                    "location": location,
                    "area": area,
                    "property_type": property_type,
                    "beds": beds,
                    "baths": baths,
                    "furnishing": furnishing,
                    "added_on": added_on,
                    "reference_no": reference_no,
                    "purpose": purpose,
                    "trucheck_date": trucheck_date,
                    "breadcrumb": breadcrumb,
                    "image": image,
                }
            else:
                print(response.status_code)

    except Exception as e:
        print(f"An error occurred: {e}")


product_links = get_product_links(BASE_URL)
data = list(get_product(product_links, BASE_URL))


with open(JSON_FILE_PATH,"w") as file:
    json.dump(data, file, indent=4)

with open(CSV_FILE_PATH, "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=data[0].keys())
    writer.writeheader()
    for row in data:
        writer.writerow(row)

print("Completed Scussfully")
