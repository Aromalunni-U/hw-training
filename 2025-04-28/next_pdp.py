from parsel import Selector


path = "2025-04-28/next_website_pdp.html"

with open(path, "r") as file:
    content = file.read()

selector = Selector(text=content)

product_name = selector.xpath("//h1[@data-testid='product-title']/text()").get()
unique_id = selector.xpath("//span[@data-testid='product-code']/text()").get()
price = selector.xpath("//div[@data-testid='product-now-price']/span/text()").get()
review = selector.xpath("//span[@data-testid='rating-style-badge']/text()").getall()[1] or "No reviews"
color = selector.xpath("//span[@data-testid='selected-colour-label']/text()").get() 
images = selector.xpath("//img[@class='percy-hide']/@src").getall()

product_description = selector.xpath(
    "//div[@data-testid='item-description-tone-of-voice']/p/text()"
).get()

rating = selector.xpath(
    "//h3[contains(@class, 'MuiTypography-root') and contains(@class, 'MuiTypography-subtitle1')]/text()"
).get()

sizes = selector.xpath("//li[@role='option']/text()").getall()


composition = selector.xpath(
    "//div[@data-testid='item-description-tone-of-voice']/ul/li/text()"
).getall()


print(f"Product Name: {product_name}")
print(f"Unique ID: {unique_id}")
print(f"Price: {price}")
print(f"Review: {review}")
print(f"Color: {color}")
print(f"Images: {images}")
print(f"Rating: {rating}")
print(f"Size: {sizes}")
print(f"Description: {product_description}")
print(f"Composition: {composition}")