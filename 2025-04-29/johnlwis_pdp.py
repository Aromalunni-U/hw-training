from parsel import Selector

path = "2025-04-29/johnlewis_pdp.html"

with open(path,"r") as file:
    content = file.read()

selector = Selector(text=content)

product_name = selector.xpath("//h1[@class='Title_title__MZ67h']/div/text()").get()
unique_id = selector.xpath("//p[@data-testid='description:code']/strong/text()").getall()[1]
price = selector.xpath("//span[@class='price_price__now__bNSvu']/text()").get()
color = selector.xpath("//span[@class='colour_c-colour__label-text__W4AnQ']/text()").getall()
brand = selector.xpath("//span[@class='Title_otherBrand__TOt2R']/text()").get()
review = selector.xpath("//span[contains(@class, 'RatingAndReviews_ratingText__g55DD')]/text()").get()
images = selector.xpath("//img[@class='Thumbnails_thumbnailImage__CAJCm']/@src").getall()
breadcrumbs = selector.xpath("//ol[@class='breadcrumbs-carousel--list']/li/a/text()").getall()
sizes = selector.xpath("//li[@data-testid='size:option']/a/text()").getall()

product_description = selector.xpath(
    "//div[@class='ProductDescriptionAccordion_descriptionContent__yd_yu']/p/text()"
).getall()

rating = selector.xpath("//span[contains(@class, 'ratings-reviews-ui_RatingsSummary__fraction')]/text()").get()

material_composition= selector.xpath(
    "(//dt[@class='ProductSpecificationAccordion_productSpecificationListValue__UNc6e'])[3]/text()"
).get()

care_instructions = selector.xpath(
    "(//dt[@class='ProductSpecificationAccordion_productSpecificationListValue__UNc6e'])[last()]/text()"
).get()

currency = selector.xpath("//span[@class='price_price__now__bNSvu']/text()").get()
currency = currency[0] if currency else None


print(f"Product Name: {product_name}")
print(f"Unique ID: {unique_id}")    
print(f"Price: {price}")
print(f"Currency: {currency}")
print(f"Review: {review}")
print(f"Color: {color}")
print(f"Images: {images}")
print(f"Rating: {rating}")
print(f"Size: {sizes}")
print(f"Description: {product_description}")
print(f"Material Composition: {material_composition}")
print(f"Breadcrumbs: {breadcrumbs}")
print(f"Brand: {brand}")
print(f"Care Instructions: {care_instructions}")