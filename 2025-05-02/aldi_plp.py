import requests
from parsel import Selector

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" 
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


def get_products_link(url):
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            selector = Selector(response.text)
            product_links = selector.xpath(
                "//div[@class='product-tile']//a[contains(@class,'product-tile__link')]/@href"
            ).getall()

            return product_links
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print(f"Status code: {response.status_code}")