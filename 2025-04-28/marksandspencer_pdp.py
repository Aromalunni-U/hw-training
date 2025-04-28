import requests
from parsel import Selector


url = "https://www.marksandspencer.com/pure-linen-shirt/p/clp60723644?color=WHITE#intid=pid_pg1pip48g4r1c3%7Cprodflag_plp_ts_CBS_2"

response = requests.get(url)

if response.status_code == 200:
    
    try:    
      selector = Selector(response.text)

      product_name = selector.xpath("//h1[@class='media-0_headingSm__aysOm']/text()").get()
      selling_price = selector.xpath("//p[contains(@class, 'media-0_headingSm')]/text()").get()
      brand = selector.xpath("//p[contains(@class, 'brand-title_title')]/text()").get()
      care = selector.xpath('//p[contains(@class, "product-details_careText__t_RPG")]/text()').getall()
      images = selector.xpath("//img[@data-tagg='gallery-image']/@src").getall()
      unique_id = "".join(selector.xpath(
         "//p[@class='media-0_textXs__ZzHWu']//text()"
      ).getall()).split(":")[-1]

      size = selector.xpath(
            "//ul[contains(@class, 'selector-group-array_array')]"
            "/li//span[@class='media-0_body__yf6Z_']/text()"
      ).getall()

      review = selector.xpath(
         "//span[contains(@class,'media-0_strong__aXigV')"
         "and contains(@class,'media-0_textSm__Q52Mz')]/text()"
      ).get()

      color = selector.xpath(
         "//ul[contains(@class, 'selector-group-array_array__hAWxQ')]"
         "/li/label[contains(@aria-label, 'colour option')]/@aria-label"
      ).getall()

      material_composition = selector.xpath(
         "//div[@class='product-details_compositionContainer__xgv9c']"
         "/p[@class='media-0_textSm__Q52Mz']/text()"
      ).get()

      style = selector.xpath(
         "//p[contains(@class, 'media-0_textSm__Q52Mz') and"
         "contains(@class, 'product-details_dimension__dy_UN')]/text()" 
      ).getall()

      breadcrumb = selector.xpath("//ul[contains(@class, 'breadcrumb_list')]/li/a/text()").getall()

      product_description = selector.xpath("//p[@class='media-0_textSm__Q52Mz']/text()").getall()

      review = selector.xpath("//h4[@class='media-0_headingMd__1TuR5']/text()").get()

     
      print(f"Product Name: {product_name}")
      print(f"Unique ID: {unique_id}")
      print(f"Price: {selling_price}")
      print(f"Pdp url: {url}")
      print(f"Brand: {brand}")
      print(f"Care: {care}")
      print(f"Images: {images}")
      print(f"Size: {size}")
      print(f"Review: {review}")
      print(f"Color: {color}")
      print(f"Composition: {material_composition}")
      print(f"Style: {style}")
      print(f"Breadcrumb: {breadcrumb}")
      print(f"Product Description: {product_description}")
      print(f"Review: {review}")


    except Exception as e:
        print(f"An error occurred: {e}")  
