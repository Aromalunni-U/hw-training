import scrapy
from .aldi_parse_code import parse_product_details

class AldiSpider(scrapy.Spider):
    name = "aldi"
    allowed_domains = ["aldi.us"]
    start_urls = [
        "https://www.aldi.us/products/fresh-produce/fresh-fruit/k/89"
    ]

    def parse(self, response):
        
        product_links = response.xpath(
            "//div[@class='product-tile']//a[contains(@class,'product-tile__link')]/@href"
        ).getall()

        for link in product_links:
            product_url = response.urljoin(link)
            yield scrapy.Request(url=product_url, callback=self.parse_product)

    
    def parse_product(self, response):
        product_data = parse_product_details(response)
        if product_data:
            yield product_data     

       