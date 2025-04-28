from parsel import Selector


path = "2025-04-28/next_website.html"

with open(path, "r") as file:
    content = file.read()

selector = Selector(text=content)


category = selector.xpath("//div[@class='esi-header-wrapper']/h1/text()").get()

product_name = selector.xpath('//p[@data-testid="product_summary_title"]/text()').getall()

images = selector.xpath('//a[contains(@class, "MuiCardMedia-root")]/img/@src').getall()

pdp_link = selector.xpath('//a[contains(@class, "MuiCardMedia-root")]/@href').getall()

print(f"Product Name: {product_name}")
print(f"Images: {images}")
print(f"Pdp Link: {pdp_link}")
print(f"Category: {category}")