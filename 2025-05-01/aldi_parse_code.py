
def parse_product_details(response):
    try:
        product_name = response.xpath(
            "//h1[@class='product-details__title']/text()"
        ).get().split(",")[0].strip()

        breadcrum = response.xpath("//nav[@aria-label='Breadcrumb']//a/text()").getall()
        price = response.xpath("//span[@class='base-price__regular']/span/text()").get()

        image = response.xpath(
            "//div/img[contains(@class,'base-image') and contains(@class,'zoom-on-hover__image')]/@src"
        ).get()

        product_description = response.xpath(
            "//div[@class='show-more__content']/div[contains(@class,'base-rich-text')]/text()"
        ).get() or "no description"

        return {
            "product_name": product_name,
            "product_link": response.url,
            "price": price,
            "image": image,
            "product_description": product_description,
            "breadcrum": breadcrum,
        }
    except Exception as e:
        print(f"Error parsing product details: {e}")