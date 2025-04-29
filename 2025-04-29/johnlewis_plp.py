from parsel import Selector



path = "2025-04-29/johnlewis_plp.html"

with open(path,"r") as file:
    content = file.read()


selector = Selector(text=content)


category = selector.xpath("//span[@class='Header_heading__main__fHBTl']/text()").get()

product_name = selector.xpath(
    "//h2[@class='title_title__Wd7Vh']/span[contains(@class, 'title_title__brand__JlYUI')]/text()"
).get()

price = selector.xpath("//span[@class='price_price__now__bNSvu']/text()").get()
pdp_url = selector.xpath("//a[@class='product-card_c-product-card__link___7IQk']/@href").get()
pagination = selector.xpath("//ul[@data-testid='pagination-footer']//a/@href").get()


print(f"Category: {category}")
print(f"Product Name: {product_name}")
print(f"PDP URL: {pdp_url}")
print(f"Price: {price}")
print(f"Pagination: {pagination}")